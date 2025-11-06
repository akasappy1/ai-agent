import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result =subprocess.run(["python3", os.path.abspath(full_path)] + args, capture_output=True,
                               cwd=working_directory, timeout=30, text=True)
        result_string = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        if result.stdout.strip() == "" and result.stderr.strip() == "":
            result_string = "No output produced"
        if result.returncode != 0:
            result_string += f"\nProcess exited with code {result.returncode}"
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"