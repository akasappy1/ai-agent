import os
import sys
import argparse
from dotenv import load_dotenv
from time import sleep
from google import genai
from google.genai import types
from call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


parser = argparse.ArgumentParser(
    prog="ai-agent", description="An AI agent built on gemini"
)
parser.add_argument('prompt', type=str, help="the prompt you want to use")
parser.add_argument('-v', '--verbose', action='store_true', default=False, help="If set to true, your prompt and the token costs will display in the console")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make and execute a function call plan. 
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

If you need file info or to run code, call the appropriate tool before answering
and continue until done. All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls as it is automatically
injected for security reasons."""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def main():
    load_dotenv()
    api_key =  os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not set in .env")
    
    client = genai.Client(api_key=api_key)
    print("Hello from ai-agent!")
    
    args = parser.parse_args()
    user_prompt = args.prompt.strip()
    if not user_prompt:
        raise Exception("No prompt provided, exiting program.)")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    i = 0
    while i < 20:
        try:
            answer = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                )
                )
            i += 1

            for candidate in answer.candidates:
                messages.append(candidate.content)
            calls = []
            fc = None
            for p in answer.candidates[0].content.parts:
                fc = getattr(p, "function_call", None)
                if fc:
                    calls.append(fc)
            if calls:
                responses = []
                for fc in calls:
                    response = call_function(fc)
                    responses.append(types.Part(function_response=response.parts[0].function_response))
                messages.append(
                    types.Content(role="user", parts=responses))
                if args.verbose:
                    for response in responses:
                        print(f"-> {response.parts[0].function_response.response}")
                continue
            else:
                if answer.text:
                    print(answer.text)
                    break
            # if args.verbose:
            #     print(f"User prompt: {user_prompt}")
            #     print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
            #     print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")
            print(answer.text)
            

        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                sleep(3)
            else:
                print(f"Sorry, something went wrong. Error: {e}")
                exit(1)
    
    

    
    # if args.verbose:
    #     print(f"User prompt: {user_prompt}")
    #     print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
    #     print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e}")
        exit(1)