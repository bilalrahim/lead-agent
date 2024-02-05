from langchain_community.chat_models import ChatCohere
from langchain_community.llms import Cohere
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAI

import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extractInformationUsingCohere(prompt):
    """
    Extract information using the Cohere API with a given prompt.

    Parameters:
    - prompt (str): The prompt for extracting information.

    Returns:
    str: Extracted information content.
    """
    print(f'Extracting information using Cohere with prompt: {prompt}')
    cohere_chat_model = ChatCohere(cohere_api_key=COHERE_API_KEY)
    current_message = [HumanMessage(content=prompt)]
    response = cohere_chat_model(current_message)
    
    print(f"Response: {response.content.rstrip('.')}")
    return response.content.rstrip('.')

def getAnswerUsingCohere(prompt, max_tokens, temperature):
    """
    Generate an opener using Cohere model with the given prompt.

    Parameters:
    - prompt (str): Prompt for generating opener.
    - max_tokens (int): Maximum number of tokens in the generated text.
    - temperature (float): Temperature parameter for text generation.

    Returns:
    str: Generated opener text.
    """
    try:
        print(f'Generating opener using Cohere with prompt: {prompt}')
        llm = Cohere(model="command", cohere_api_key=COHERE_API_KEY, temperature=temperature, max_tokens=max_tokens)
        output = llm.invoke(prompt)
        print(f'Generated opener using Cohere: {output}')
        return output
    except Exception as e:
        print(f"Error generating opener using Cohere: {e}")
        return None
    

def generateResponseUsingOpenAI(prompt):
    """
    Generate using OpenAI model with the given prompt.

    Parameters:
    - prompt (str): Prompt for generating opener.

    Returns:
    tuple: Tuple containing generated email subject and body.
    """
    try:
        llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)

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