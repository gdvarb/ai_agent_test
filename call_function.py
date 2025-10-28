from functions.tools import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content,
    ]
)
