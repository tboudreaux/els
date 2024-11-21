import magic

def is_binary(file_path):
    """
    Uses libmagic to determine if a file is binary or text.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if binary, False if text.
    """
    try:
        file_type = magic.from_file(file_path, mime=True)
        if file_type is None:
            # Unable to determine, treat as binary
            return True
        if 'charset=binary' in file_type or not file_type.startswith('text/'):
            return True   # It's a binary file
        else:
            return False  # It's a text file
    except Exception as e:
        print(f"Error determining file type: {e}")
        return True  # Treat unreadable files as binary

