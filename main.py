import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from system_prompt import system_prompt
from functions.tools import schema_get_files_info




available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"


def main():
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )
        try:
            print(response.function_calls)
            if response.function_calls: 
                function_call_part = response.function_calls[0]
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_res = function_call_part.name
                print(response.text)

                return f"Calling function: {function_call_part.name}({function_call_part.args})"
            if sys.argv[2] and sys.argv[2] == "--verbose":
                print(f"User prompt: {user_prompt} \n Response: {response.text} \n Prompt tokens: {response.usage_metadata.prompt_token_count} \n Response tokens: {response.usage_metadata.candidates_token_count}") 
        except:
            print(response.text)
    else:
        print("No prompt was given")
        sys.exit(1)





if __name__ == "__main__":
    main()
