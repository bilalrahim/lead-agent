import pandas as pd
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from services.LLM.getAnswerUsingCohere import getAnswerUsingCohere
from modules.savePromptAsMarkdown import savePromptAsMarkdown

input_csv = "leads.csv"
prompt_output_file = "prompts.md"
email_output_csv = "opener_output.csv"


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


def process_opener_agent():
    """
    Process the opener agent for each lead in the input CSV file.
    """
    output_data = []
    temperature = 0.2
    try:
        df = pd.read_csv(input_csv)
        for index, row in df.iterrows():
            print(f"Processing lead {index + 1} of {len(df)}")
            lead = row.to_dict()

            prompt_info = {
                "looking_for": lead['Looking For'],
                "antematter_description": "is a Software firm that develops and improves cutting-edge solutions using Blockchain & AI with one guarantee: maximum performance, in every sense of the word.",
                "lead_name": lead['Name'],
                "company_name": lead['Organizaton'],
                "company_size": lead['Company Size'],
            }

            subject_prompt = generate_email_subject_prompt(prompt_info)
            email_prompt = generate_email_body_prompt(prompt_info)

            savePromptAsMarkdown([subject_prompt, email_prompt], prompt_output_file)

            subject, body = generate_opener_email(subject_prompt, email_prompt, temperature)

            if subject is not None and body is not None:
                output_data.append({
                    "Email Subject": subject,
                    "Email Body": body,
                })

        # Save generated emails to CSV
        pd.DataFrame(output_data).to_csv(email_output_csv, index=False)
    except Exception as e:
        print(f"Error processing opener agent: {e}")


if __name__ == "__main__":
    process_opener_agent()