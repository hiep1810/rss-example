def get_file_text_length(file_path):
    """
    Calculates the length of the text content in a given file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The number of characters in the file's text content,
             or -1 if the file cannot be opened or read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content)
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return -1
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return -1

# Example usage:
file_name = "vietstock_all_articles.csv"

text_length = get_file_text_length(file_name)

if text_length != -1:
    print(f"The length of the text in '{file_name}' is: {text_length} characters.")