#!/usr/bin/python3
import subprocess
import os


# Get cwd
cwd = os.getcwd()
print("Current working directory path:", cwd)

# Traverse through the current working directory and print the name of each file and directory
for index, item in enumerate(os.listdir(cwd)):
    full_path = os.path.join(cwd, item)
    # Check if the item is a directory or a file
    if os.path.isdir(full_path):
        print("Directory:", item)
    else:
        print("File:", item)
        input_filename = item
        output_filename = f'{index}.png'

        # ImageMagick config
        percentage = "50%"
        width = 1200
        height = 900

        # Build the command to resize the image using ImageMagick
        command = [
            "convert",       # the ImageMagick command
            input_filename,  # the input filename
            "-resize",       # the resize option
            f"{width}x{height}",  # the desired output dimensions
            output_filename  # the output filename
        ]

        subprocess.run(command)
        os.remove(input_filename)
        print(f"File {input_filename} was deleted!, {output_filename} was created")

