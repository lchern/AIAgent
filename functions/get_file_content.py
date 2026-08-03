import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the content of a specified file relative to the working directory. Truncates the file in case it's too large.",
        "parameters": {
            "type": "object",
            "required": "file_path",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    file_content_string = ""
    body = ""
    try:
        abs_path = os.path.abspath(working_directory)
    except Exception as e:
        return (
            f"Error: an unexpected error occurred while calling 'os.path.abspath': {e}"
        )
    try:
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
    except Exception as e:
        return (
            f"Error: an unexpected error occurred while calling 'os.path.normpath': {e}"
        )
    try:
        valid_target_dir = os.path.commonpath([abs_path, target_path])
    except Exception as e:
        return f"\tError: an unexpected error occurred while calling 'os.path.commonpath': {e}"
    if not valid_target_dir == abs_path:
        body = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_path):
        body = f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    result = body + file_content_string
    return result
