import logging
import traceback
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from services.prompts import generate_missing_detail_prompt
from services.connector import (
    generate_response,
    is_requesting_more_information,
    does_contain_budget,
    does_contain_scope
)
from modules.savePromptAsMarkdown import savePromptAsMarkdown


# Constants
INPUT_CSV = "leads.csv"
OUTPUT_OPENER_CSV = "opener_output.csv"
PROMPT_OUTPUT_FILE = "escalator_prompts.md"
RESPONSE_OUTPUT_CSV = "escalator_output.csv"
TEMPERATURE = 0.2

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_lead(lead, index):
    """
    Process a lead and determine the appropriate response.

    Parameters:
    - lead (dict): Dictionary containing lead information.

    Returns:
    dict: Dictionary with lead status and agent response.
    """
    contains_request, is_requesting_more_information_prompt = is_requesting_more_information(lead["Lead Response"])
    contains_budget, does_contain_budget_prompt = does_contain_budget(lead["Lead Response"])
    contains_scope, does_contain_scope_prompt = does_contain_scope(lead["Lead Response"])

    if contains_request == "Yes":
        return {"Lead Status": "ESCALATED", "Agent Response": "NULL"}
    elif contains_budget == "Yes" or contains_scope == "Yes":
        return {"Lead Status": "ESCALATED", "Agent Response": "NULL"}
    elif contains_budget == "No" and contains_scope == "No":
        missing_detail_prompt = generate_missing_detail_prompt("scope and budget")
    elif contains_budget == "No" and contains_scope == "Yes":
        missing_detail_prompt = generate_missing_detail_prompt("budget")
    else:
        missing_detail_prompt = generate_missing_detail_prompt("scope")

    savePromptAsMarkdown(
        [is_requesting_more_information_prompt, does_contain_budget_prompt, does_contain_scope_prompt, missing_detail_prompt],
        PROMPT_OUTPUT_FILE, index
    )
    response = generate_response(missing_detail_prompt, 400, TEMPERATURE)
    return {"Lead Status": "NOT-ESCALATED", "Agent Response": response}

def process_escalator_agent():
    """
    Process the escalator agent for each lead in the input CSV file.
    """
    output_data = []

    try:
        df = pd.read_csv(INPUT_CSV)
        openerDf = pd.read_csv(OUTPUT_OPENER_CSV)

        for index, row in df.iterrows():
            logger.info(f"Processing lead {index + 1} of {len(df)}")
            lead = row.to_dict()
            lead_result = process_lead(lead, index)

            output_data.append({
                "Model Name": "Cohere's command",
                "Temperature": TEMPERATURE,
                "Lead Information": lead["Lead Response"],
                "Prompt": openerDf.loc[index, "Prompt"],
                "Email Subject": openerDf.loc[index, "Email Subject"],
                "Email Body": openerDf.loc[index, "Email Body"],
                "Lead Response": lead["Lead Response"],
                "Lead Status": lead_result["Lead Status"],
                "Agent Response": lead_result["Agent Response"],
            })

        # Save generated emails to CSV
        pd.DataFrame(output_data).to_csv(RESPONSE_OUTPUT_CSV, index=False)
    except Exception as e:
        logger.error(f"Error processing escalater agent: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    process_escalator_agent()