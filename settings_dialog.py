from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QSpinBox, QCheckBox, QPushButton, QTabWidget,
                            QWidget, QFormLayout, QComboBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPalette, QColor

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ClipCache Settings")
        self.setMinimumWidth(400)
        
        self.settings = QSettings("ClipCache", "Settings")
        
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # General settings tab
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        # History size
        self.history_size = QSpinBox()
        self.history_size.setRange(10, 1000)
        self.history_size.setSingleStep(10)
        self.history_size.setValue(self.settings.value("max_history_size", 100, type=int))
        general_layout.addRow("Maximum history items:", self.history_size)
        
        # Auto-start
        self.auto_start = QCheckBox("Start ClipCache when Windows starts")
        self.auto_start.setChecked(self.settings.value("auto_start", False, type=bool))
        general_layout.addRow("Auto-start:", self.auto_start)
        
        # Force to front
        self.force_to_front = QCheckBox("Always keep window on top of other windows")
        self.force_to_front.setChecked(self.settings.value("force_to_front", False, type=bool))
        general_layout.addRow("Always on top:", self.force_to_front)
        
        # Image capture
        self.image_capture = QCheckBox()
        self.image_capture.setChecked(self.settings.value("image_capture", True, type=bool))
        general_layout.addRow("Capture images:", self.image_capture)
        
        # Auto-clear
        self.auto_clear = QCheckBox()
        self.auto_clear.setChecked(self.settings.value("auto_clear", False, type=bool))
        general_layout.addRow("Auto-clear clipboard:", self.auto_clear)
        
        self.auto_clear_time = QSpinBox()
        self.auto_clear_time.setRange(1, 60)
        self.auto_clear_time.setValue(self.settings.value("auto_clear_time", 5, type=int))
        general_layout.addRow("Auto-clear after (minutes):", self.auto_clear_time)
        
        tabs.addTab(general_tab, "General")
        
        # Appearance tab
        appearance_tab = QWidget()
        appearance_layout = QFormLayout(appearance_tab)
        
        # Theme
        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System"])
        current_theme = self.settings.value("theme", "System")
        self.theme.setCurrentText(current_theme)
        appearance_layout.addRow("Theme:", self.theme)
        
        # Theme preview
        self.theme_preview = QLabel()
        self.theme_preview.setMinimumHeight(100)
        self.theme_preview.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")
        appearance_layout.addRow("Preview:", self.theme_preview)
        
        # Update preview when theme changes
        self.theme.currentTextChanged.connect(self.update_theme_preview)
        self.update_theme_preview(current_theme)
        
        tabs.addTab(appearance_tab, "Appearance")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
    def update_theme_preview(self, theme_name):
        """Update the theme preview based on the selected theme."""
        if theme_name == "Light":
            self.theme_preview.setStyleSheet("""
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
            """)
            self.theme_preview.setText("Light Theme Preview")
        elif theme_name == "Dark":
            self.theme_preview.setStyleSheet("""
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 10px;
            """)
            self.theme_preview.setText("Dark Theme Preview")
        else:  # System
            palette = self.theme_preview.palette()
            self.theme_preview.setStyleSheet("""
                background-color: palette(window);
                color: palette(window-text);
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 10px;
            """)
            self.theme_preview.setText("System Theme Preview")
        
    def save_settings(self):
        self.settings.setValue("max_history_size", self.history_size.value())
        self.settings.setValue("auto_start", self.auto_start.isChecked())
        self.settings.setValue("force_to_front", self.force_to_front.isChecked())
        self.settings.setValue("image_capture", self.image_capture.isChecked())
        self.settings.setValue("auto_clear", self.auto_clear.isChecked())
        self.settings.setValue("auto_clear_time", self.auto_clear_time.value())
        self.settings.setValue("theme", self.theme.currentText())
        
        self.accept() 