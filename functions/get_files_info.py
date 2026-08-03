import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    body = ""
    try:
        abs_path = os.path.abspath(working_directory)
    except Exception as e:
        return (
            f"Error: an unexpected error occurred while calling 'os.path.abspath': {e}"
        )
    try:
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
    except Exception as e:
        return (
            f"Error: an unexpected error occurred while calling 'os.path.normpath': {e}"
        )
    try:
        valid_target_dir = os.path.commonpath([abs_path, target_dir])
    except Exception as e:
        return f"\tError: an unexpected error occurred while calling 'os.path.commonpath': {e}"
    if not valid_target_dir == abs_path:
        body = f'\tError: Cannot list "{directory}" as it is outside the permitted working directory\n'
    elif not os.path.isdir(target_dir):
        body = f'Error: "{directory}" is not a directory\n'
    else:
        for item in os.listdir(target_dir):
            body += f"  - {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}\n"
    header = f'Result for "{directory}" directory:\n'
    result = header.replace('"."', 'current') + body
    return result
