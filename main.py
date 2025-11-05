import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


parser = argparse.ArgumentParser(
    prog="ai-agent", description="An AI agent built on gemini"
)
parser.add_argument('text_input', type=str, help="the prompt you want to use")
parser.add_argument('-v', '--verbose', action='store_true', default=False, help="If set to true, your prompt and the token costs will display in the console")


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
    answer = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")
    print(answer.text)
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e}")
        exit(1)