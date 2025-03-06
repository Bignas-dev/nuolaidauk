import os
from barcode import Code128
from barcode.writer import SVGWriter

print("Input data")
code_data = input("> ")

print("File name")
file_name = input("> ")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, f"{file_name}.svg")

with open(file_path, "wb") as f:
    Code128(code_data, writer=SVGWriter()).write(f)

print(f"Barcode saved in {file_path}")
