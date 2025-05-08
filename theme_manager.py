from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QSettings
import platform
from styles import get_light_stylesheet, get_dark_stylesheet

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.settings = QSettings("ClipCache", "Settings")
        self.current_theme = self.settings.value("theme", "System")
        
        # Define color schemes
        self.light_theme = {
            "Window": QColor(240, 240, 240),
            "WindowText": QColor(0, 0, 0),
            "Base": QColor(255, 255, 255),
            "AlternateBase": QColor(245, 245, 245),
            "Text": QColor(0, 0, 0),
            "Button": QColor(240, 240, 240),
            "ButtonText": QColor(0, 0, 0),
            "Highlight": QColor(0, 120, 215),
            "HighlightedText": QColor(255, 255, 255),
            "Link": QColor(0, 102, 204),
            "LinkVisited": QColor(128, 0, 128),
            "ToolTipBase": QColor(255, 255, 220),
            "ToolTipText": QColor(0, 0, 0),
        }
        
        self.dark_theme = {
            "Window": QColor(53, 53, 53),
            "WindowText": QColor(255, 255, 255),
            "Base": QColor(35, 35, 35),
            "AlternateBase": QColor(45, 45, 45),
            "Text": QColor(255, 255, 255),
            "Button": QColor(53, 53, 53),
            "ButtonText": QColor(255, 255, 255),
            "Highlight": QColor(0, 120, 215),
            "HighlightedText": QColor(255, 255, 255),
            "Link": QColor(42, 130, 218),
            "LinkVisited": QColor(180, 130, 180),
            "ToolTipBase": QColor(70, 70, 70),
            "ToolTipText": QColor(255, 255, 255),
        }
        
        # Apply initial theme
        self.apply_theme(self.current_theme)
        
    def apply_theme(self, theme_name):
        """Apply the specified theme to the application."""
        self.current_theme = theme_name
        self.settings.setValue("theme", theme_name)
        
        if theme_name == "System":
            # Check if system is using dark mode
            if self._is_system_dark_mode():
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
        elif theme_name == "Dark":
            self._apply_dark_theme()
        else:  # Light
            self._apply_light_theme()
            
    def _apply_light_theme(self):
        """Apply light theme to the application."""
        # Apply palette
        palette = QPalette()
        for role_name, color in self.light_theme.items():
            role = getattr(QPalette, role_name)
            palette.setColor(role, color)
        self.app.setPalette(palette)
        
        # Apply stylesheet
        self.app.setStyleSheet(get_light_stylesheet())
        
    def _apply_dark_theme(self):
        """Apply dark theme to the application."""
        # Apply palette
        palette = QPalette()
        for role_name, color in self.dark_theme.items():
            role = getattr(QPalette, role_name)
            palette.setColor(role, color)
        self.app.setPalette(palette)
        
        # Apply stylesheet
        self.app.setStyleSheet(get_dark_stylesheet())
        
    def _is_system_dark_mode(self):
        """Check if the system is using dark mode."""
        if platform.system() == "Windows":
            # On Windows 10/11, we can check the registry
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                winreg.CloseKey(key)
                return value == 0  # 0 means dark mode
            except:
                # Fallback to light theme if we can't determine
                return False
        else:
            # For other platforms, default to light theme
            return False
            
    def get_current_theme(self):
        """Return the current theme name."""
        return self.current_theme 