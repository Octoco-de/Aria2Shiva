import os

async def constrain_text_to_length(text, length):
    result = text
    if len(result) > length:
        result = f"{result[:length]}..."
    return result


def validateDirectory(directory):
    print("directory", directory)
    # Check if the directory exists, and create it if it doesn't
    expanded_directory = os.path.abspath(os.path.expanduser(directory))
    os.makedirs(expanded_directory, exist_ok=True)