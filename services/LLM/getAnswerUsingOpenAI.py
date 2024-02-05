from langchain_openai import OpenAI

openai_api_key = "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"


def generateResponseUsingOpenAI(prompt):
    """
    Generate using OpenAI model with the given prompt.

    Parameters:
    - prompt (str): Prompt for generating opener.

    Returns:
    tuple: Tuple containing generated email subject and body.
    """
    try:
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

        # Generate email subject (limited to 30 characters)
        response_subject = llm(prompt + " Subject:", max_tokens=30)
        subject = response_subject.strip().capitalize()

        # Generate email body (limited to 150 tokens, approximately 3 paragraphs)
        response_body = llm(prompt + "\n\nBody:", max_tokens=150)
        body = response_body.strip()

        return subject, body
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None, None