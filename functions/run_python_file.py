import os
import subprocess
from google.genai import types

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

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Uses the subprocess.run method to run a python file, within the working directory, and captures output and error codes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file that subprocess.run will run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual parameter required by the specified Python file."
                ),
                description="The list of parameters of the specified Python file."
            )
        }
    )
)