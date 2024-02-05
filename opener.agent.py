import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from modules.savePromptAsMarkdown import savePromptAsMarkdown
from services.prompts import generate_email_subject_prompt, generate_email_body_prompt
from services.connector import generate_opener_email

input_csv = "leads.csv"
prompt_output_file = "prompts.md"
email_output_csv = "opener_output.csv"

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