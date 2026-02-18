import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory with optional command-line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        # Ensure file is inside working directory
        if not absolute_file_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Ensure file exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Ensure file is a Python file
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        # Non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # Capture stdout
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")

        # Capture stderr
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")

        # No output at all
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

