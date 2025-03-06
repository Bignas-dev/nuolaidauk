#!/usr/bin/env python3

import os
import sys
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.utils import platform
from app.main import BarcodeApp

def main():
    if platform == "android":
        try:
            from android.permissions import request_permissions, Permission

            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
            )
        except ImportError:
            pass

    Config.set("kivy", "keyboard_mode", "system")
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")

    app_dir = os.path.dirname(os.path.abspath(__file__))
    if app_dir not in sys.path:
        sys.path.append(app_dir)

    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    try:
        app = BarcodeApp()
        app.run()
    except Exception as e:
        error_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "error_log.txt"
        )
        with open(error_path, "w") as f:
            f.write(f"Error: {str(e)}")


if __name__ == "__main__":
    main()

