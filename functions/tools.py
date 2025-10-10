import os

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

    with open(full_path, "r") as f:
        file_content_string = f.read()
        if len(file_content_string) > MAX_CHARS:
            f.seek(0)
            file_content_string = f.read(MAX_CHARS)
            print(f'File Content:\n{file_content_string} \n[... File "{file_path} truncated to 10000 characters"]')
        else:
            print(file_content_string)
            return f"File Content:\n{file_content_string}"

def get_files_info(working_directory, directory="."):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_absolute_path, directory))

    if not os.path.isdir(full_path):
        print(f'Error: "{directory}" is not a directory')
        return f'Error: "{directory}" is not a directory'
            
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        files =os.listdir(full_path)
        file_string = ""
        for file in files:
            if file.startswith("."):
                continue
            file_path = full_path + f"/{file}"
            try:
                file_string = file_string + f'- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n'
            except Exception as e:
                print(f"An error occured: {e}")
                return f"Error: {e}"
        print(file_string)
        return file_string

def write_file(working_directory, file_path, content):
    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory')
        return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f'Made directory: {full_path}')

    try:
        with open(full_path, 'w') as f:
            f.write(content + '\n')
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters writen)')
    except Exception as e:
        print(f'An error occured: {e}')
        return f'An error occured: {e}'

    
