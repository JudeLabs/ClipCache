def get_light_stylesheet():
    """Return the light theme stylesheet."""
    return """
    QMainWindow {
        background-color: #f8f9fa;
    }
    
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
    }
    
    QLineEdit {
        padding: 10px 12px;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background-color: white;
        selection-background-color: #2196F3;
        selection-color: white;
    }
    
    QLineEdit:focus {
        border: 1px solid #2196F3;
        background-color: #ffffff;
    }
    
    QListWidget {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: white;
        padding: 4px;
    }
    
    QListWidget::item {
        padding: 12px;
        margin: 2px 0;
        border-radius: 6px;
        border: none;
    }
    
    QListWidget::item:selected {
        background-color: #e3f2fd;
        color: #1976D2;
    }
    
    QListWidget::item:hover {
        background-color: #f5f5f5;
    }
    
    QPushButton {
        padding: 10px 16px;
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0D47A1;
    }
    
    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: white;
        padding: 16px;
    }
    
    QTabBar::tab {
        padding: 10px 20px;
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        border-bottom: 1px solid white;
        font-weight: 500;
    }
    
    QCheckBox {
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #e0e0e0;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #2196F3;
        border: 2px solid #2196F3;
    }
    
    QSpinBox {
        padding: 8px;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background-color: white;
    }
    
    QSpinBox:focus {
        border: 1px solid #2196F3;
    }
    
    QComboBox {
        padding: 8px 12px;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background-color: white;
    }
    
    QComboBox:focus {
        border: 1px solid #2196F3;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    
    QComboBox::down-arrow {
        image: url(down-arrow.png);
        width: 12px;
        height: 12px;
    }
    
    QLabel {
        color: #424242;
    }
    
    QMenu {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 4px;
    }
    
    QMenu::item {
        padding: 8px 24px;
        border-radius: 4px;
    }
    
    QMenu::item:selected {
        background-color: #e3f2fd;
        color: #1976D2;
    }
    
    QMenu::separator {
        height: 1px;
        background-color: #e0e0e0;
        margin: 4px 0;
    }
    """

def get_dark_stylesheet():
    """Return the dark theme stylesheet."""
    return """
    QMainWindow {
        background-color: #1e1e1e;
    }
    
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        color: #e0e0e0;
    }
    
    QLineEdit {
        padding: 10px 12px;
        border: 1px solid #404040;
        border-radius: 6px;
        background-color: #2d2d2d;
        color: #e0e0e0;
        selection-background-color: #2196F3;
        selection-color: white;
    }
    
    QLineEdit:focus {
        border: 1px solid #2196F3;
        background-color: #333333;
    }
    
    QListWidget {
        border: 1px solid #404040;
        border-radius: 8px;
        background-color: #2d2d2d;
        padding: 4px;
    }
    
    QListWidget::item {
        padding: 12px;
        margin: 2px 0;
        border-radius: 6px;
        border: none;
    }
    
    QListWidget::item:selected {
        background-color: #0D47A1;
        color: #ffffff;
    }
    
    QListWidget::item:hover {
        background-color: #404040;
    }
    
    QPushButton {
        padding: 10px 16px;
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0D47A1;
    }
    
    QTabWidget::pane {
        border: 1px solid #404040;
        border-radius: 8px;
        background-color: #2d2d2d;
        padding: 16px;
    }
    
    QTabBar::tab {
        padding: 10px 20px;
        background-color: #1e1e1e;
        border: 1px solid #404040;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #2d2d2d;
        border-bottom: 1px solid #2d2d2d;
        font-weight: 500;
    }
    
    QCheckBox {
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #404040;
        border-radius: 4px;
        background-color: #2d2d2d;
    }
    
    QCheckBox::indicator:checked {
        background-color: #2196F3;
        border: 2px solid #2196F3;
    }
    
    QSpinBox {
        padding: 8px;
        border: 1px solid #404040;
        border-radius: 6px;
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QSpinBox:focus {
        border: 1px solid #2196F3;
    }
    
    QComboBox {
        padding: 8px 12px;
        border: 1px solid #404040;
        border-radius: 6px;
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QComboBox:focus {
        border: 1px solid #2196F3;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    
    QComboBox::down-arrow {
        image: url(down-arrow.png);
        width: 12px;
        height: 12px;
    }
    
    QLabel {
        color: #e0e0e0;
    }
    
    QMenu {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 6px;
        padding: 4px;
    }
    
    QMenu::item {
        padding: 8px 24px;
        border-radius: 4px;
    }
    
    QMenu::item:selected {
        background-color: #0D47A1;
        color: #ffffff;
    }
    
    QMenu::separator {
        height: 1px;
        background-color: #404040;
        margin: 4px 0;
    }
    """ 