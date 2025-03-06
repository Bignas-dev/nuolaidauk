#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Create directory for images if it doesn't exist
os.makedirs('data/images', exist_ok=True)

# Function to create a simple icon
def create_icon():
    # Create a 512x512 image with blue background (matching app's primary color)
    img = Image.new('RGBA', (512, 512), (51, 153, 230, 255))  # Blue color
    draw = ImageDraw.Draw(img)
    
    # Draw a white rounded rectangle
    draw.rounded_rectangle([(100, 100), (412, 412)], radius=50, fill=(255, 255, 255, 255))
    
    # Draw a barcode-like pattern
    bar_x = 150
    for i in range(8):
        width = 20 if i % 2 == 0 else 30
        draw.rectangle([(bar_x, 150), (bar_x + width, 362)], fill=(0, 0, 0, 255))
        bar_x += width + 10
    
    # Save the icon
    img.save('data/images/icon.png', 'PNG')
    
    # Create smaller versions for Android
    sizes = [(192, 192), (144, 144), (96, 96), (72, 72), (48, 48), (36, 36)]
    for size in sizes:
        small_img = img.resize(size, Image.LANCZOS)
        small_img.save(f'data/images/icon_{size[0]}x{size[1]}.png', 'PNG')
    
    print("Icon created successfully!")

# Function to create a simple splash screen
def create_splash():
    # Create a splash screen with the same blue background
    img = Image.new('RGBA', (1280, 1920), (51, 153, 230, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a white rounded rectangle
    draw.rounded_rectangle([(300, 760), (980, 1160)], radius=50, fill=(255, 255, 255, 255))
    
    # Draw a barcode-like pattern
    bar_x = 400
    for i in range(10):
        width = 30 if i % 2 == 0 else 50
        draw.rectangle([(bar_x, 830), (bar_x + width, 1090)], fill=(0, 0, 0, 255))
        bar_x += width + 15
    
    # Save the splash screen
    img.save('data/images/presplash.png', 'PNG')
    print("Splash screen created successfully!")

if __name__ == "__main__":
    create_icon()
    create_splash()