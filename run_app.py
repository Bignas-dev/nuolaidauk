#!/usr/bin/env python3

import os
import sys

# Add current directory to path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Launch the app
from app.main import BarcodeApp

if __name__ == "__main__":
    BarcodeApp().run()
