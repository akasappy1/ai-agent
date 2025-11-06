import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        contents = sorted(os.listdir(full_path))
        file_list = ""
        for item in contents:
            entry_path = os.path.join(full_path, item)
            file_size = os.path.getsize(entry_path)
            file_is_directory = os.path.isdir(entry_path)
            file_info = f"- {item}: file_size={file_size} bytes, is_dir={file_is_directory}"
            file_list += file_info + "\n"
        if directory == ".":
            dir_name = "current" 
        else:
            dir_name = directory
        pretty_return = f"Result for {dir_name} directory:\n{file_list}"
        return pretty_return
    except Exception as e:
        return f"Error: {e}"

