from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

AVAILABLE_FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func_name = function_call_part.name
    func_args = function_call_part.args 
    func_args["working_directory"] = "./calculator"
    actual_func = AVAILABLE_FUNCTIONS.get(func_name)
    if actual_func is None:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    func_result = actual_func(**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": func_result}
            )
        ]
    )