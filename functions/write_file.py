import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
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
        result = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_path):
        result = f'Error: Cannot write to "{file_path}" as it is a directory'
    else:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        result = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    return result
