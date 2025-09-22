def windows_to_wsl_path(windows_path):
    """
    Convert a Windows path to WSL path format.

    Args:
        windows_path (str): Windows file path (e.g., r"C:\\Users\\...")

    Returns:
        str: WSL equivalent path (e.g., "/mnt/c/Users/...")

    Examples:
        >>> windows_to_wsl_path(r"C:\\Users\\John\\Documents\\file.txt")
        '/mnt/c/Users/John/Documents/file.txt'

        >>> windows_to_wsl_path(r"D:\\Projects\\my project\\data.csv")
        '/mnt/d/Projects/my project/data.csv'
    """

    # Remove quotes if present
    path = windows_path.strip('"\'')

    # Handle UNC paths (\\server\share) - not directly supported in WSL
    if path.startswith('\\\\'):
        raise ValueError("UNC paths (\\\\server\\share) are not directly supported in WSL")

    # Extract drive letter and path
    if len(path) >= 2 and path[1] == ':':
        drive_letter = path[0].lower()
        remaining_path = path[2:]
    else:
        raise ValueError(f"Invalid Windows path format: {windows_path}")

    # Convert backslashes to forward slashes
    remaining_path = remaining_path.replace('\\', '/')

    # Remove leading slash if present
    if remaining_path.startswith('/'):
        remaining_path = remaining_path[1:]

    # Construct WSL path
    wsl_path = f"/mnt/{drive_letter}"
    if remaining_path:
        wsl_path += f"/{remaining_path}"

    return wsl_path