#!/usr/bin/env python3

import os
import sys
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.utils import platform

# Fix import issue by adding parent directory to sys.path
app_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(app_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.main import BarcodeApp

def main():
    if platform == "android":
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except ImportError:
            pass

    # Set window size for desktop
    Config.set("kivy", "keyboard_mode", "system")
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")

    # Handle PyInstaller packaging
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
        
    # Run the app
    BarcodeApp().run()

if __name__ == "__main__":
    main()

