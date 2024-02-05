def savePromptAsMarkdown(prompts, file_path):
    """
    Save prompts to a markdown file.

    Parameters:
    - prompts (list): List of prompts to be saved.
    - file_path (str): Path to the markdown file.

    Returns:
    None
    """
    try:
        with open(file_path, "a") as f:  # Use 'a' for append mode
            for prompt in prompts:
                # Add markdown bullet points for each prompt
                f.write(f"- {prompt}\n")
    except Exception as e:
        print(f"Error saving prompts to markdown file: {e}")