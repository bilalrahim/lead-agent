from langchain.prompts.prompt import PromptTemplate

def generate_email_subject_prompt(lead_info):
    """
    Generate a prompt for the email subject.

    Parameters:
    - lead_info (dict): Dictionary containing lead information.

    Returns:
    str: Email subject prompt.
    """
    template = """ 
            Output a subject for a cold email no more than 30 characters to {lead_name} 
            of {company_name} from Antematter {antematter_description} who are looking for a Software Consultancy Provider.
            In the output only give me the subject nothing else.
            """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=[
            "lead_name",
            "company_name",
            "antematter_description",
        ])

    return prompt_template.format(lead_name=lead_info["lead_name"], company_name=lead_info["company_name"],
                                  antematter_description=lead_info["antematter_description"])


def generate_email_body_prompt(lead_info):
    """
    Generate a prompt for the email body.

    Parameters:
    - lead_info (dict): Dictionary containing lead information.

    Returns:
    str: Email body prompt.
    """
    template = """
            Write a cold email to {lead_name} of {company_name} who are looking for a Software Consultancy Provider for
            the following reasons {looking_for}. The email is to introduce Antematter which is {antematter_description}. 
            Inquire about {company_name} potential scope and budget.
            
            The output email should have the following format:
            - Introduction
            - Antematter's value proposition
            - Asking for more information regarding the scope and budget
          """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[
            "antematter_description",
            "lead_name",
            "company_name",
            "looking_for"
        ])

    return prompt_template.format(antematter_description=lead_info["antematter_description"],
                                  lead_name=lead_info["lead_name"], company_name=lead_info["company_name"],
                                  looking_for=lead_info["looking_for"])


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

def generate_missing_detail_prompt(missing_detail):
    """
    Generate a prompt for writing an email inquiry about missing project details.

    Parameters:
    - missing_detail (str): The missing detail (e.g., scope or budget).

    Returns:
    str: The generated missing detail prompt.
    """
    template = """
            Write an email inquiring a user about their projects {missing_detail}.
            Use a professional tone. 
            """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[
            "missing_detail",
        ])
    
    return prompt_template.format(missing_detail=missing_detail)