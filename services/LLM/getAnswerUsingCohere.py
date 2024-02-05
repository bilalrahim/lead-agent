from langchain_community.llms import Cohere
import os
cohere_api_key = os.getenv("COHERE_API_KEY")

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
        llm = Cohere(model="command", cohere_api_key=cohere_api_key, temperature=temperature, max_tokens=max_tokens)
        output = llm.invoke(prompt)
        print(f'Generated opener using Cohere: {output}')
        return output
    except Exception as e:
        print(f"Error generating opener using Cohere: {e}")
        return None