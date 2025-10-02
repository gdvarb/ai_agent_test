import os
def get_files_info(working_directory, directory="."):
    working_absolute_path = os.path.abspath(working_directory)

    directory_absolute_path = os.path.abspath(directory)
    if not os.path.isdir(directory_absolute_path):
        print(f'Error: "{directory}" is not a directory')
        return f'Error: "{directory}" is not a directory'
        

    full_path = os.path.join(working_directory, directory_absolute_path)
    
    if not full_path.startswith(working_absolute_path):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    else:
        print(f'"{directory}" is a valid working directory')
        files =os.listdir(full_path)
        print(files)
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
    

    

#get_files_info(working_directory="..", directory= "..")
