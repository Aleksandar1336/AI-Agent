from functions.get_files_info import get_files_info


if __name__ == "__main__":
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    if result.startswith("Error:"):
        print(f"  {result}")
    else:
        for line in result.split("\n"):
            print(f"  {line}")

    print("\nResult for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    if result.startswith("Error:"):
        print(f"  {result}")
    else:
        for line in result.split("\n"):
            print(f"  {line}")

    print("\nResult for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.split("\n"):
            print(f"  {line}")

    print("\nResult for '../' directory:")
    result = get_files_info("calculator", "../")
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.split("\n"):
            print(f"  {line}")

