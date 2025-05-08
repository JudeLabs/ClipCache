import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu,
                            QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                            QAction, QStyle, QTabWidget, QLabel, QSpinBox,
                            QCheckBox, QPushButton, QHBoxLayout, QLineEdit,
                            QDialog, QFormLayout, QComboBox, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QSize, QByteArray, QBuffer, QIODevice, QPropertyAnimation, QEasingCurve, QPoint, QSettings
from PyQt5.QtGui import QIcon, QPixmap, QClipboard, QImage, QColor
import win32clipboard
from PIL import Image
import io
from secure_database import SecureDatabase
from theme_manager import ThemeManager
from settings_dialog import SettingsDialog
from icon import create_clipboard_icon
from license_dialog import LicenseDialog

class AnimatedListItem(QListWidgetItem):
    def __init__(self, text, item_id, parent=None):
        super().__init__(text, parent)
        self.item_id = item_id
        self.is_pinned = False
        self.is_deleting = False
        self.is_sensitive = False

class ClipCache(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClipCache")
        self.setMinimumSize(400, 600)
        
        # Set application icon
        self.setWindowIcon(create_clipboard_icon())
        
        # Initialize clipboard monitoring
        self.clipboard = QApplication.clipboard()
        self.last_clipboard_content = None
        self.monitoring_paused = False
        self.is_copying_from_history = False  # Flag to prevent duplicate entries
        
        # Initialize secure database
        self.db = SecureDatabase()
        
        # Setup UI
        self.setup_ui()
        self.setup_system_tray()
        
        # Start clipboard monitoring
        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        
        # Load settings
        self.load_settings()
        
        # Apply initial window flags based on settings
        self.update_window_flags()
        
        # Setup auto-clear timer
        self.setup_auto_clear_timer()
        
    def setup_ui(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search clipboard history...")
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.ExtendedSelection)  # Enable multi-select
        self.history_list.itemClicked.connect(self.copy_to_clipboard)
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        self.history_list.setSpacing(4)  # Add spacing between items
        layout.addWidget(self.history_list)
        
        # Load initial history
        self.load_history()
        
    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(create_clipboard_icon())
        
        # Create tray menu
        self.tray_menu = QMenu()
        
        # Toggle history window
        self.show_action = self.tray_menu.addAction("✓ History Window Visible")
        self.show_action.triggered.connect(self.toggle_window)
        
        self.pause_action = self.tray_menu.addAction("Toggle Monitoring")
        self.pause_action.triggered.connect(self.toggle_monitoring)
        
        clear_action = self.tray_menu.addAction("Clear History")
        clear_action.triggered.connect(self.clear_history)
        
        settings_action = self.tray_menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        
        license_action = self.tray_menu.addAction("License Information")
        license_action.triggered.connect(self.show_license_info)
        
        self.tray_menu.addSeparator()
        
        exit_action = self.tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        
    def on_clipboard_change(self):
        if self.monitoring_paused or self.is_copying_from_history:
            return
            
        # Get clipboard content
        mime_data = self.clipboard.mimeData()
        
        if mime_data.hasText():
            content = mime_data.text()
            if content != self.last_clipboard_content:
                self.db.save_item("text", content)
                self.last_clipboard_content = content
                self.load_history()  # Reload history after saving
        elif mime_data.hasImage():
            image = self.clipboard.image()
            if image:
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QIODevice.WriteOnly)
                image.save(buffer, "PNG")
                if byte_array != self.last_clipboard_content:
                    self.db.save_item("image", byte_array.data())
                    self.last_clipboard_content = byte_array.data()
                    self.load_history()  # Reload history after saving
                    
    def load_history(self):
        self.history_list.clear()
        items = self.db.get_history()
        
        for item_id, content_type, content, timestamp, is_pinned, is_sensitive, expiration_time in items:
            if content_type == "text":
                preview = content[:100].decode() + "..." if len(content) > 100 else content.decode()
            else:  # Image
                try:
                    # Create thumbnail from image data
                    image = QImage()
                    image.loadFromData(content)
                    
                    # Create a scaled pixmap for the thumbnail
                    pixmap = QPixmap.fromImage(image)
                    scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # Create a widget to hold the thumbnail and text
                    item_widget = QWidget()
                    layout = QHBoxLayout(item_widget)
                    layout.setContentsMargins(4, 4, 4, 4)
                    
                    # Add thumbnail
                    thumbnail_label = QLabel()
                    thumbnail_label.setPixmap(scaled_pixmap)
                    layout.addWidget(thumbnail_label)
                    
                    # Add image info
                    info_label = QLabel(f"Image ({image.width()}x{image.height()})")
                    layout.addWidget(info_label)
                    
                    # Create list item
                    item = AnimatedListItem("", item_id)
                    item.is_pinned = bool(is_pinned)
                    item.is_sensitive = bool(is_sensitive)
                    
                    # Set icon based on content type and pinned status
                    if is_pinned:
                        item.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
                    elif is_sensitive:
                        item.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))
                    else:
                        item.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                    
                    # Set the custom widget
                    self.history_list.addItem(item)
                    self.history_list.setItemWidget(item, item_widget)
                    continue
                except Exception as e:
                    print(f"Error loading image: {e}")
                    preview = "[Image]"
            
            # Handle text items or failed image loads
            item = AnimatedListItem(preview, item_id)
            item.is_pinned = bool(is_pinned)
            item.is_sensitive = bool(is_sensitive)
            
            # Set icon based on content type and pinned status
            if is_pinned:
                item.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
            elif is_sensitive:
                item.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))
            elif content_type == "text":
                item.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
            else:
                item.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                
            self.history_list.addItem(item)
            
    def copy_to_clipboard(self, item):
        if not isinstance(item, AnimatedListItem):
            return
            
        content_type, content = self.db.get_item(item.item_id)
        if content:
            # Set flag to prevent duplicate entry
            self.is_copying_from_history = True
            
            if content_type == "text":
                self.clipboard.setText(content.decode())
            elif content_type == "image":
                image = QImage()
                image.loadFromData(content)
                self.clipboard.setImage(image)
                
            # Reset flag after a short delay to ensure clipboard change event has been processed
            QTimer.singleShot(100, self.reset_copying_flag)
                
    def reset_copying_flag(self):
        """Reset the flag that prevents duplicate entries when copying from history."""
        self.is_copying_from_history = False
                
    def filter_history(self, text):
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
            
    def toggle_monitoring(self):
        self.monitoring_paused = not self.monitoring_paused
        # Update the action text with status indicator
        if self.monitoring_paused:
            self.pause_action.setText("⚠️ Monitoring Disabled")
        else:
            self.pause_action.setText("✓ Monitoring Enabled")
        
    def clear_history(self):
        """Clear all unpinned items from history."""
        self.db.clear_history()
        self.load_history()
        
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Apply theme if changed
            new_theme = dialog.theme.currentText()
            if new_theme != self.theme_manager.get_current_theme():
                self.theme_manager.apply_theme(new_theme)
            # Update window flags if always-on-top setting changed
            self.update_window_flags()
            # Enforce history limit if it was changed
            self.db.enforce_history_limit(dialog.history_size.value())
            # Reload history to reflect any changes
            self.load_history()
            # Update auto-clear timer interval if needed
            self.update_auto_clear_timer()
        
    def load_settings(self):
        # Initialize theme manager
        self.theme_manager = ThemeManager(QApplication.instance())
        
        # Apply initial window flags based on settings
        self.update_window_flags()
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ClipCache",
            "Application minimized to system tray",
            QSystemTrayIcon.Information,
            2000
        )
        
    def show_context_menu(self, position):
        items = self.history_list.selectedItems()
        if not items:
            return
            
        menu = QMenu()
        
        # Copy action (only enabled for single selection)
        copy_action = menu.addAction("Copy")
        copy_action.setEnabled(len(items) == 1)
        copy_action.triggered.connect(lambda: self.copy_to_clipboard(items[0]))
        
        # Pin/Unpin action (only enabled for single selection)
        if len(items) == 1:
            if items[0].is_pinned:
                pin_action = menu.addAction("Unpin")
            else:
                pin_action = menu.addAction("Pin")
            pin_action.triggered.connect(lambda: self.toggle_pin(items[0]))
        
        # Delete action (enabled for single or multiple selections)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_items(items))
        
        menu.exec_(self.history_list.mapToGlobal(position))
        
    def toggle_pin(self, item):
        if not isinstance(item, AnimatedListItem):
            return
            
        self.db.toggle_pin(item.item_id)
        self.load_history()
        
    def delete_items(self, items):
        """Delete multiple items from the history."""
        if not items:
            return
            
        try:
            for item in items:
                if isinstance(item, AnimatedListItem):
                    self.db.delete_item(item.item_id)
            self.load_history()
        except Exception as e:
            print(f"Error deleting items: {e}")
            
    def close(self):
        """Close the application completely."""
        self.db.close()
        self.tray_icon.hide()  # Hide the tray icon
        QApplication.quit()  # Quit the entire application

    def showEvent(self, event):
        """Handle window show event."""
        super().showEvent(event)
        
        # Update the show action text
        self.show_action.setText("✓ History Window Visible")
        
        # Check if force to front is enabled
        settings = QSettings("ClipCache", "Settings")
        if settings.value("force_to_front", False, type=bool):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.activateWindow()
            self.raise_()
            
    def hideEvent(self, event):
        """Handle window hide event."""
        super().hideEvent(event)
        # Update the show action text
        self.show_action.setText("👁️ History Window Hidden")

    def toggle_window(self):
        if self.isVisible():
            self.hide()
            self.show_action.setText("👁️ History Window Hidden")
        else:
            self.show()
            self.show_action.setText("✓ History Window Visible")

    def update_window_flags(self):
        """Update window flags based on settings."""
        settings = QSettings("ClipCache", "Settings")
        if settings.value("force_to_front", False, type=bool):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()  # Need to show the window again after changing flags

    def setup_auto_clear_timer(self):
        """Setup timer to check for expired items."""
        self.auto_clear_timer = QTimer(self)
        self.auto_clear_timer.timeout.connect(self.check_expired_items)
        self.auto_clear_timer.start(60000)  # Check every minute
        
    def check_expired_items(self):
        """Check for and remove expired items."""
        # Get current settings
        settings = QSettings("ClipCache", "Settings")
        auto_clear = settings.value("auto_clear", False, type=bool)
        
        if auto_clear:
            # This will trigger the expiration check in get_history
            self.load_history()
            
            # Update the timer interval to check more frequently
            self.auto_clear_timer.setInterval(1000)  # Check every second
        else:
            self.auto_clear_timer.stop()

    def update_auto_clear_timer(self):
        """Update the auto-clear timer based on settings."""
        settings = QSettings("ClipCache", "Settings")
        auto_clear = settings.value("auto_clear", False, type=bool)
        auto_clear_time = settings.value("auto_clear_time", 5, type=int)
        
        if auto_clear:
            # Set timer interval to half of the auto-clear time to ensure timely cleanup
            interval = max(1000, auto_clear_time * 30000)  # Minimum 1 second, maximum 30 minutes
            self.auto_clear_timer.setInterval(interval)
            self.auto_clear_timer.start()
        else:
            self.auto_clear_timer.stop()

    def show_license_info(self):
        """Show the license information dialog."""
        dialog = LicenseDialog(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(create_clipboard_icon())
    window = ClipCache()
    window.show()
    sys.exit(app.exec_()) 