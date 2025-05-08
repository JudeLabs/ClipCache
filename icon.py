from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QSize

def create_clipboard_icon(size=64):
    """Create a custom clipboard icon for the application."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Clipboard base
    painter.setPen(QPen(QColor("#2196F3"), 2))
    painter.setBrush(QBrush(QColor("#2196F3")))
    painter.drawRoundedRect(8, 8, size-16, size-16, 8, 8)
    
    # Clipboard top
    painter.setPen(QPen(QColor("#1976D2"), 2))
    painter.setBrush(QBrush(QColor("#1976D2")))
    painter.drawRoundedRect(size//2-16, 4, 32, 12, 4, 4)
    
    # Lines
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(QColor("white")))
    
    # First line
    painter.drawRoundedRect(16, size//2-16, size-32, 6, 3, 3)
    
    # Second line
    painter.drawRoundedRect(16, size//2, size-32, 6, 3, 3)
    
    # Third line
    painter.drawRoundedRect(16, size//2+16, size-32, 6, 3, 3)
    
    painter.end()
    
    return QIcon(pixmap) 