import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        # Absolute working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize full file path
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Ensure target_path is inside working_directory
        valid_target = (
            os.path.commonpath([working_dir_abs, target_path])
            == working_dir_abs
        )

        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file safely (limit size)
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            # Check if file was truncated
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"

