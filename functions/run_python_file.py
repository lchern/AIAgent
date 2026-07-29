import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    output = ""
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
        output = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_path):
        output = f'Error: "{file_path}" does not exist or is not a regular file'
    elif not target_path[-3:] == ".py":
        output = f'Error: "{file_path}" is not a Python file'
    else:
        try:
            command = ["python", target_path]
            if args is not None:
                command.extend(args)
            result = subprocess.run(command, timeout=30, capture_output=True, text=True, cwd=abs_path)
            if result.returncode != 0:
                output += f"Process exited with code {result.returncode}\n"
            elif result.stderr == "" and result.stdout == "":
                output += "No output produced\n"
            else:
                output += f"STDOUT: {result.stdout}\n"
                output += f"STDERR: {result.stderr}\n"
        except Exception as e:
            return f"Error: executing Python file: {e}"
    return output
