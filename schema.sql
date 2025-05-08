-- ClipCache Database Schema

-- Main clipboard history table
CREATE TABLE clipboard_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type TEXT NOT NULL,  -- 'text' or 'image'
    content BLOB,                -- The actual clipboard content
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_pinned BOOLEAN DEFAULT 0,
    is_sensitive BOOLEAN DEFAULT 0,
    expiration_time DATETIME     -- NULL for pinned items, timestamp for auto-clear
);

-- Indexes for better performance
CREATE INDEX idx_timestamp ON clipboard_history(timestamp);
CREATE INDEX idx_is_pinned ON clipboard_history(is_pinned);
CREATE INDEX idx_expiration ON clipboard_history(expiration_time);

-- Example of how the table would be used:
-- INSERT INTO clipboard_history (content_type, content, is_pinned) 
-- VALUES ('text', 'Sample text content', 0); 