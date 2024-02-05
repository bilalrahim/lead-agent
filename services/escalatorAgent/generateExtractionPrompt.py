from langchain.prompts.prompt import PromptTemplate
def generate_extraction_prompt(response, question):
    """
    Generate a prompt for extracting information from a given response.

    Parameters:
    - response (str): The response text containing information.
    - question (str): The specific question related to the information.

    Returns:
    str: The generated extraction prompt.
    """
    template = """ 
            I am going to pass you some information below and a question.
            Only use this specific information to answer the question.
            The answer format should be a yes or no, that is it.

            Question: {question}
            Paragraph: {response}
            """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=[
            "question",
            "response",
        ])

    return prompt_template.format(question=question, response=response)