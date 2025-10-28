import os
import sys
import subprocess
from google import genai
from google.genai import types

schema_get_file_content= types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    working_directory_abs_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory_abs_path, file_path))
    print(full_path)
    
    if not full_path.startswith(working_directory_abs_path):
        print(f'Error: Cannot read "{file_path}" as it is outside of the working directory')
        return f'Error: Cannot read "{file_path}" as it is outside of the working directory'

    if not os.path.isfile(full_path):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                f.seek(0)
                file_content_string = f.read(MAX_CHARS)
                print(f'File Content:\n{file_content_string} \n[... File "{file_path} truncated to 10000 characters"]')
            else:
                print(file_content_string)
                return f"File Content:\n{file_content_string}"
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_absolute_path, directory))

    if not os.path.isdir(full_path):
        print(f'Error: "{directory}" is not a directory')
        return f'Error: "{directory}" is not a directory'
            
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:    
        files_info = []
        for filename in os.listdir(full_path):
            filepath = os.path.join(full_path, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        print("\n".join(files_info))
        return "\n".join(files_info)    
    except Exception as e:
        print(f"An error occured: {e}")
        return f"Error listing files: {e}"

schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file to the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="What should be written to the file.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be written to relative to the working directory. If file does not exist it will be created. Constrained to working directory"

            )
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory')
        return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'
    
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except Exception as e:
            print(f"Error: creating directory: {e}")
            return f"Error: creating directory: {e}"

    if os.path.exists(full_path) and os.path.isdir(full_path):
        print(f"Error: '{file_path}' is a directory, not a file")
        return f"Error: '{file_path}' is a directory, not a file"

    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"


    
schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Parameter value"
                ),
                description="Array of parameters that should be passed to the function. Defaults to empty list.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be executed. Constrained to working directory"
            )
        },
        required=["file_path"]
    ),
)   

def run_python_file(working_directory, file_path, args=[]):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory')
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'

    if not os.path.isfile(full_path):
        print(f'Error: File "{file_path}" not found')
        return f'Error: File "{file_path}" not found'

    
    dirname = os.path.dirname(full_path)
    if not os.path.exists(dirname):
        print(f'Error: "{file_path} not found."') 
        return f'Error: "{file_path} not found."'

    #print("Full path:",full_path)
    if not full_path.endswith(".py"):
        print(f'Error: "{file_path}" is not a Python file.')
        return f'Error: "{file_path}" is not a Python file.'

    function_args = [sys.executable]
    function_args.extend([full_path])
    function_args.extend(args)
    #print('Function args:',function_args)
    try:
        function_output = subprocess.run(function_args, capture_output=True, timeout=30, text=True)
        if not function_output:
            print("No output produced.")

        if function_output.stdout:
            print(f'STDOUT: {function_output.stdout}')
        elif function_output.stderr:
            print(f'STDERR: {function_output.stderr}')

    except Exception as e:
        print(f'Error: executing Python file: {e}')


def call_function(function_call_part, verbose=False):
    function = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content
    }

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    if function_name not in function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args = function_call_part.args
    function_args["working_directory"] = "./calculator"

    function_result = function[function_name](**function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


