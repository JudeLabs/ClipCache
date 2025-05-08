from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextBrowser, 
                             QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("License Information")
        self.setMinimumSize(600, 400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create text browser for license information
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        
        # Add license information
        license_text = """
        <h2>ClipCache License Information</h2>
        
        <h3>ClipCache Application</h3>
        <p>Copyright © 2024 JudeLabs</p>
        <p>All rights reserved.</p>
        
        <h3>Third-Party Libraries</h3>
        
        <h4>PyQt5</h4>
        <p>Copyright © Riverbank Computing Limited</p>
        <p>License: GPL v3 or Commercial License</p>
        <p>Website: <a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a></p>
        
        <h4>SQLite</h4>
        <p>Public Domain</p>
        <p>Website: <a href="https://www.sqlite.org/">https://www.sqlite.org/</a></p>
        
        <h4>PIL (Python Imaging Library)</h4>
        <p>Copyright © 1997-2011 by Secret Labs AB</p>
        <p>License: PIL Software License</p>
        <p>Website: <a href="https://python-pillow.org/">https://python-pillow.org/</a></p>
        
        <h4>pywin32</h4>
        <p>Copyright © 1996-2008, Greg Stein and Mark Hammond</p>
        <p>License: Python Software Foundation License</p>
        <p>Website: <a href="https://github.com/mhammond/pywin32">https://github.com/mhammond/pywin32</a></p>
        
        <h3>Disclaimer</h3>
        <p>This software is provided "as is", without warranty of any kind, express or implied, 
        including but not limited to the warranties of merchantability, fitness for a particular 
        purpose and noninfringement.</p>
        """
        
        self.text_browser.setHtml(license_text)
        layout.addWidget(self.text_browser)
        
        # Add close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout) 