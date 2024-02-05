from langchain_community.chat_models import ChatCohere
from langchain_core.messages import HumanMessage
import os

cohere_api_key = os.getenv("COHERE_API_KEY")

def extractInformationUsingCohere(prompt):
    """
    Extract information using the Cohere API with a given prompt.

    Parameters:
    - prompt (str): The prompt for extracting information.

    Returns:
    str: Extracted information content.
    """
    print(f'Extracting information using Cohere with prompt: {prompt}')
    cohere_chat_model = ChatCohere(cohere_api_key=cohere_api_key)
    current_message = [HumanMessage(content=prompt)]
    response = cohere_chat_model(current_message)
    
    print(f"Response: {response.content.rstrip('.')}")
    return response.content.rstrip('.')