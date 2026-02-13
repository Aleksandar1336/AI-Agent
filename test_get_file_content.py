from functions.get_file_content import get_file_content
from config import MAX_CHARS


if __name__ == "__main__":
    print("Testing lorem.txt (should truncate):")
    content = get_file_content("calculator", "lorem.txt")

    if content.startswith("Error:"):
        print(content)
    else:
        print(f"Length returned: {len(content)}")
        print("Ends with truncation message:",
              content.endswith(f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'))

    print("\nTesting main.py:")
    print(get_file_content("calculator", "main.py"))

    print("\nTesting pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\nTesting /bin/cat (should error):")
    print(get_file_content("calculator", "/bin/cat"))

    print("\nTesting missing file (should error):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

