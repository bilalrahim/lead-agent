import logging
import traceback
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from modules.savePromptAsMarkdown import savePromptAsMarkdown
from services.prompts import generate_email_subject_prompt, generate_email_body_prompt
from services.connector import generate_opener_email

# Constants
INPUT_CSV = "leads.csv"
PROMPT_OUTPUT_FILE = "opener_prompts.md"
EMAIL_OUTPUT_CSV = "opener_output.csv"
TEMPERATURE = 0.2

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_lead_opener(lead, index):
    """
    Process the opener agent for a given lead.

    Parameters:
    - lead (dict): Dictionary containing lead information.

    Returns:
    dict: Dictionary with email subject and body.
    """
    prompt_info = {
        "looking_for": lead['Looking For'],
        "antematter_description": "is a Software firm that develops and improves cutting-edge solutions using Blockchain & AI with one guarantee: maximum performance, in every sense of the word.",
        "lead_name": lead['Name'],
        "company_name": lead['Organizaton'],
        "company_size": lead['Company Size'],
    }

    subject_prompt = generate_email_subject_prompt(prompt_info)
    email_prompt = generate_email_body_prompt(prompt_info)

    savePromptAsMarkdown([subject_prompt, email_prompt], PROMPT_OUTPUT_FILE, index)

    subject, body = generate_opener_email(subject_prompt, email_prompt, TEMPERATURE)

    if subject is not None and body is not None:
        return {"EmailSubject": subject, "EmailBody": body, "Prompt": "Subject Prompt" + subject_prompt + "Email: Prompt" + email_prompt}
    else:
        return None

def process_opener_agent():
    """
    Process the opener agent for each lead in the input CSV file.
    """
    output_data = []

    try:
        df = pd.read_csv(INPUT_CSV)
        for index, row in df.iterrows():
            logger.info(f"Processing lead {index + 1} of {len(df)}")
            lead = row.to_dict()
            lead_result = process_lead_opener(lead, index + 1)

            if lead_result is not None:
                output_data.append(
                    {
                        "Model Name": "Cohere's command",
                        "Temperature": TEMPERATURE,
                        "Lead Information": lead['Looking For'],
                        "Prompt": lead_result["Prompt"].replace("\n", " "),
                        "Email Subject": lead_result["EmailSubject"],
                        "Email Body": lead_result["EmailBody"]
                    }
                )

        # Save generated emails to CSV
        pd.DataFrame(output_data).to_csv(EMAIL_OUTPUT_CSV, index=False)
    except Exception as e:
        logger.error(f"Error processing opener agent: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    process_opener_agent()