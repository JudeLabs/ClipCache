import os
import sqlite3
import re
import stat
from PyQt5.QtCore import QSettings

class SecureDatabase:
    def __init__(self):
        self.db_path = os.path.join(os.path.expanduser("~"), ".clipcache", "history.db")
        
        # Create directory with secure permissions
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._secure_file_permissions()
        
        # Initialize database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._init_database()
        
    def _secure_file_permissions(self):
        """Set secure file permissions for the .clipcache directory and its contents."""
        clipcache_dir = os.path.dirname(self.db_path)
        
        # Secure the .clipcache directory
        os.chmod(clipcache_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        
        # Secure existing files
        if os.path.exists(self.db_path):
            os.chmod(self.db_path, stat.S_IRUSR | stat.S_IWUSR)
                
    def _init_database(self):
        """Initialize the database with tables."""
        # Create the main table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clipboard_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_type TEXT NOT NULL,
                content BLOB,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                expiration_time DATETIME,
                is_pinned BOOLEAN DEFAULT 0,
                is_sensitive BOOLEAN DEFAULT 0
            )
        ''')
        
        # Check if is_sensitive column exists, add it if it doesn't
        try:
            self.cursor.execute('SELECT is_sensitive FROM clipboard_history LIMIT 1')
        except sqlite3.OperationalError:
            print("Migrating database to add is_sensitive column...")
            # Create a temporary table with the new schema
            self.cursor.execute('''
                CREATE TABLE clipboard_history_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_type TEXT NOT NULL,
                    content BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expiration_time DATETIME,
                    is_pinned BOOLEAN DEFAULT 0,
                    is_sensitive BOOLEAN DEFAULT 0
                )
            ''')
            
            # Copy data from old table to new table
            self.cursor.execute('''
                INSERT INTO clipboard_history_new (id, content_type, content, timestamp, is_pinned)
                SELECT id, content_type, content, timestamp, is_pinned
                FROM clipboard_history
            ''')
            
            # Drop old table and rename new table
            self.cursor.execute('DROP TABLE clipboard_history')
            self.cursor.execute('ALTER TABLE clipboard_history_new RENAME TO clipboard_history')
            
        # Check if expiration_time column exists, add it if it doesn't
        try:
            self.cursor.execute('SELECT expiration_time FROM clipboard_history LIMIT 1')
        except sqlite3.OperationalError:
            print("Adding expiration_time column...")
            self.cursor.execute('ALTER TABLE clipboard_history ADD COLUMN expiration_time DATETIME')
            
        self.conn.commit()
            
    def is_sensitive_data(self, content):
        """Check if content contains sensitive information."""
        if isinstance(content, str):
            # Patterns for sensitive data
            patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                r'\b\d{16}\b',  # Credit card
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                r'password|secret|key|token|credential',  # Common sensitive words
                r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',  # IP address
                r'api[_-]?key|access[_-]?token|auth[_-]?token',  # API keys
            ]
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
        return False
        
    def sanitize_data(self, content):
        """Sanitize data before storage."""
        if isinstance(content, str):
            # Remove null bytes and other potentially dangerous characters
            content = content.replace('\0', '')
            # Remove control characters
            content = ''.join(char for char in content if ord(char) >= 32 or char == '\n')
        return content
        
    def enforce_history_limit(self, max_items):
        """Enforce the maximum history limit by removing oldest unpinned items."""
        # Get the current count
        self.cursor.execute('SELECT COUNT(*) FROM clipboard_history')
        current_count = self.cursor.fetchone()[0]
        
        if current_count > max_items:
            # Calculate how many items to remove
            items_to_remove = current_count - max_items
            
            # Delete the oldest unpinned items
            self.cursor.execute('''
                DELETE FROM clipboard_history 
                WHERE id IN (
                    SELECT id FROM clipboard_history 
                    WHERE is_pinned = 0 
                    ORDER BY timestamp ASC 
                    LIMIT ?
                )
            ''', (items_to_remove,))
            self.conn.commit()
            
    def save_item(self, content_type, content):
        """Save an item to the database."""
        # Check if content is sensitive
        is_sensitive = self.is_sensitive_data(content)
        
        # Sanitize the content
        content = self.sanitize_data(content)
        
        # Convert string content to bytes if needed
        if isinstance(content, str):
            content = content.encode()
            
        # Get auto-clear settings
        settings = QSettings("ClipCache", "Settings")
        auto_clear = settings.value("auto_clear", False, type=bool)
        auto_clear_time = settings.value("auto_clear_time", 5, type=int)
        
        # Calculate expiration time if auto-clear is enabled
        expiration_time = None
        if auto_clear:
            self.cursor.execute('''
                SELECT datetime('now', '+' || ? || ' minutes')
            ''', (auto_clear_time,))
            expiration_time = self.cursor.fetchone()[0]
        
        self.cursor.execute('''
            INSERT INTO clipboard_history (content_type, content, is_sensitive, expiration_time)
            VALUES (?, ?, ?, ?)
        ''', (content_type, content, is_sensitive, expiration_time))
        self.conn.commit()
        
        # Get the maximum history size from settings
        max_history_size = settings.value("max_history_size", 100, type=int)
        
        # Enforce the history limit
        self.enforce_history_limit(max_history_size)
        
    def get_item(self, item_id):
        """Retrieve an item from the database."""
        self.cursor.execute('SELECT content_type, content FROM clipboard_history WHERE id = ?', (item_id,))
        row = self.cursor.fetchone()
        
        if row:
            content_type, content = row
            return content_type, content
        return None, None
        
    def delete_item(self, item_id):
        """Delete an item from the database."""
        self.cursor.execute('DELETE FROM clipboard_history WHERE id = ?', (item_id,))
        self.conn.commit()
        
    def clear_history(self, include_pinned=False):
        """Clear history, optionally including pinned items."""
        if include_pinned:
            self.cursor.execute('DELETE FROM clipboard_history')
        else:
            self.cursor.execute('DELETE FROM clipboard_history WHERE is_pinned = 0')
        self.conn.commit()
        
    def get_history(self, limit=500):
        """Get history items."""
        # First, remove expired items
        self.cursor.execute('''
            DELETE FROM clipboard_history 
            WHERE expiration_time IS NOT NULL 
            AND datetime('now') > expiration_time 
            AND is_pinned = 0
        ''')
        self.conn.commit()
        
        # Then get the history, including expiration time
        self.cursor.execute('''
            SELECT id, content_type, content, timestamp, is_pinned, is_sensitive, expiration_time
            FROM clipboard_history
            ORDER BY is_pinned DESC, timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        items = []
        for row in self.cursor.fetchall():
            try:
                item_id, content_type, content, timestamp, is_pinned, is_sensitive, expiration_time = row
                if content:  # Only process if we have content
                    items.append((item_id, content_type, content, timestamp, is_pinned, is_sensitive, expiration_time))
            except Exception as e:
                print(f"Error processing history item: {e}")
                continue
        return items
        
    def toggle_pin(self, item_id):
        """Toggle the pinned status of an item and reset expiration time when unpinning."""
        # First get the current pinned status
        self.cursor.execute('SELECT is_pinned FROM clipboard_history WHERE id = ?', (item_id,))
        current_status = self.cursor.fetchone()
        
        if current_status:
            is_pinned = bool(current_status[0])
            
            # If we're unpinning, reset the expiration time
            if is_pinned:
                # Get auto-clear settings
                settings = QSettings("ClipCache", "Settings")
                auto_clear = settings.value("auto_clear", False, type=bool)
                auto_clear_time = settings.value("auto_clear_time", 5, type=int)
                
                # Calculate new expiration time if auto-clear is enabled
                expiration_time = None
                if auto_clear:
                    self.cursor.execute('''
                        SELECT datetime('now', '+' || ? || ' minutes')
                    ''', (auto_clear_time,))
                    expiration_time = self.cursor.fetchone()[0]
                
                # Update both pinned status and expiration time
                self.cursor.execute('''
                    UPDATE clipboard_history 
                    SET is_pinned = 0, expiration_time = ?
                    WHERE id = ?
                ''', (expiration_time, item_id))
            else:
                # If we're pinning, just update the pinned status
                self.cursor.execute('''
                    UPDATE clipboard_history 
                    SET is_pinned = 1, expiration_time = NULL
                    WHERE id = ?
                ''', (item_id,))
                
            self.conn.commit()
        
    def close(self):
        """Close the database connection."""
        self.conn.close() 