from services.llm import getAnswerUsingCohere, extractInformationUsingCohere
from services.prompts import generate_extraction_prompt

def generate_opener_email(subject_prompt, email_prompt, temperature):
    """
    Generate email content using subject and body prompts.

    Parameters:
    - subject_prompt (str): Prompt for the email subject.
    - email_prompt (str): Prompt for the email body.
    - temperature (float): Temperature parameter for text generation.

    Returns:
    tuple: Tuple containing generated subject and body.
    """
    try:
        cohereSubject = getAnswerUsingCohere(subject_prompt, max_tokens=30, temperature=temperature)
        cohereEmail = getAnswerUsingCohere(email_prompt, max_tokens=400, temperature=temperature)
        return cohereSubject, cohereEmail
    except Exception as e:
        print(f"Error generating opener email: {e}")
        return None, None


def generate_response(prompt, max_tokens, temperature):
    """
    Generate a response using a given prompt.

    Parameters:
    - prompt (str): The prompt for generating the response.
    - max_tokens (int): Maximum number of tokens for the generated response.
    - temperature (float): Temperature parameter for text generation.

    Returns:
    tuple: Tuple containing generated response content and response metadata.
    """
    try:
        return getAnswerUsingCohere(prompt, max_tokens, temperature)
    except Exception as e:
        print(f"Error generating escalation email: {e}")
        return None

def extract_information(prompt):
    """
    Extract information using a given prompt.

    Parameters:
    - prompt (str): The prompt for extracting information.

    Returns:
    tuple: Tuple containing extracted information content and information metadata.
    """
    try:
        return extractInformationUsingCohere(prompt)
    except Exception as e:
        print(f"Error generating escalation email: {e}")
        return None, None


def is_requesting_more_information(response):
    """
    Check if a given response contains a request for more information.

    Parameters:
    - response (str): The response text to check.

    Returns:
    str: "Yes" if a request for more information is found, otherwise "No".
    """
    question = "Does the following contain a request to schedule a call or need more information?"
    prompt = generate_extraction_prompt(response, question)
    return extract_information(prompt)


def does_contain_budget(response):
    """
    Check if a given response contains information about the budget of the project.

    Parameters:
    - response (str): The response text to check.

    Returns:
    str: "Yes" if information about the budget is found, otherwise "No".
    """
    question = "Does the following contain information about the budget of the project, and should I send a response asking about the budget?"
    prompt = generate_extraction_prompt(response, question)
    return extract_information(prompt)


def does_contain_scope(response):
    """
    Check if a given response contains information about the scope of the project.

    Parameters:
    - response (str): The response text to check.

    Returns:
    str: "Yes" if information about the scope is found, otherwise "No".
    """
    question = "Does the following contain information about the scope of the project?"
    prompt = generate_extraction_prompt(response, question)
    return extract_information(prompt)
    