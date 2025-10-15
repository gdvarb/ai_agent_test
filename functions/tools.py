import os
import sys
import subprocess
from google import genai
from google.genai import types

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

def write_file(working_directory, file_path, content):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory')
        return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'

    dirname = os.path.dirname(full_path)
    #print(f'Directory name is: {dirname}')

    if not os.path.exists(dirname):
        os.makedirs(dirname)
        #print(f'Made directory: {dirname}')

    try:
        with open(full_path, 'w') as f:
            f.write(content + '\n')
            #print(f'Successfully wrote to "{file_path}" ({len(content)} characters writen)')
            print(f"'{len(content)} characters written'")
            return f"'{len(content)} characters written'"
    except Exception as e:
        print(f"'Error:'")
        return f"'An error occured: {e}'"

    
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


