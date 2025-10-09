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
            #print(file_content_string + f'[...File "{file_path} truncated at 10000 characters"]')
        else:
            print(file_content_string)
            return f"File Content:\n{file_content_string}"
