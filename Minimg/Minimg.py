#!/usr/bin/python3
import subprocess
import os
import argparse
import datetime
import hashlib

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", help="Naming the directory the converted files saved")
    options = parser.parse_args()
    if not options.name:
        parser.error("[-] Please specify a name for directory, use --help for more info.")
    return options

def read_directory():
    cwd = os.getcwd()
    list_of_files = os.listdir(cwd)

    return list_of_files, cwd

def make_directory(name):
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print("[-] A directory is already existed. Program exitted")
        exit()
    return os.getcwd()+"/"+name

def minimize_file(file, directory, num, hashstr):
    input_filename = file
    num = '{:02d}'.format(num)
    output_filename = f'{num}_{hashstr}.png'

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
    os.rename(output_filename, os.path.join(directory, output_filename))
    print("[+] File converted : "+output_filename)

def gen_hash():
    # Get the current date and time
    now = datetime.datetime.now()

    now_str = now.isoformat()
    hash_obj = hashlib.sha256(now_str.encode())
    hash_str = hash_obj.hexdigest()
    
    return hash_str

def main():
    files, cwd = read_directory()
    files.sort()
    print(files) 
    options = get_arguments()
    directory_path = make_directory(options.name)


    file_num = 0
    for file in files:
        full_path = os.path.join(cwd, file)
        # Check if the item is a directory or a file
        if os.path.isdir(full_path):
            print("[-] Skip the directory:", file)
        else:
            print("[+] Detected the File:", file)
            file_num+=1
            hashstr = gen_hash()
            minimize_file(file, directory_path, file_num, hashstr)
            
if __name__ == "__main__":
    main()


