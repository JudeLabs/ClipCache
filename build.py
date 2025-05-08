import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    print("Building ClipCache executable...")
    
    # Ensure PyInstaller is installed
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Convert SVG to ICO if needed
    if not os.path.exists("icon.ico"):
        print("Converting SVG to ICO...")
        subprocess.run([sys.executable, "-m", "pip", "install", "cairosvg"], check=True)
        subprocess.run([sys.executable, "-m", "cairosvg", "icon.svg", "-o", "icon.ico"], check=True)
    
    # Build the executable
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=icon.ico",
        "--name=ClipCache",
        "--add-data=icon.ico;.",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=cryptography",
        "--hidden-import=PIL",
        "--hidden-import=win32clipboard",
        "clipcache.py"
    ], check=True)
    
    print("Build complete! Executable is in the dist directory.")

if __name__ == "__main__":
    build_executable() 