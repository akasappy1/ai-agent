import os
import pathlib

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(directory)
    full_working = os.path.abspath(working_directory)
    if not full_path.startswith(full_working):
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(directory):
        raise Exception(f'Error: "{directory}" is not a directory')
    contents = os.listdir(directory)
    file_list = ""
    for item in contents:
        filename = os.path.basename(item)
        file_size = os.path.getsize(item)
        file_is_directory = os.path.isdir(item)
        file_info = f"- {filename}: file_size={file_size} is_dir={file_is_directory}"
        file_list += file_info + "\n"
    return file_list
    