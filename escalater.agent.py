import pandas as pd
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from services.escalaterAgents.extractInformationUsingCohere import extractInformationUsingCohere
from services.openerAgents.generateOpenerUsingCohere import generateOpenerUsingCohere

input_csv = "leads.csv"
prompt_output_file = "prompts.md"
response_output_csv = "escalator_output.csv"

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
        return generateOpenerUsingCohere(prompt, max_tokens, temperature)
    except Exception as e:
        print(f"Error generating escalation email: {e}")
        return None, None


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


def process_escalator_agent():
    """
    Process the escalator agent for each lead in the input CSV file.
    """
    output_data = []

    try:
        df = pd.read_csv(input_csv)
        for index, row in df.iterrows():
            print(f"Processing lead {index + 1} of {len(df)}")
            lead = row.to_dict()
            contains_request = is_requesting_more_information(lead["Lead Response"])
            contains_budget = does_contain_budget(lead["Lead Response"])
            contains_scope = does_contain_scope(lead["Lead Response"])

            if contains_request == "Yes":
                output_data.append({
                    "Lead Status": "ESCALATED",
                    "Agent Response": "NULL"
                })
            elif contains_budget == "Yes" or contains_scope == "Yes":
                output_data.append({
                    "Lead Status": "Escalated",
                    "Agent Response": "NULL"
                })
            elif contains_budget == "No" and contains_scope == "No":
                missing_detail_prompt = generate_missing_detail_prompt("scope and budget")
                response = generate_response(missing_detail_prompt, 400, 0.2)
                output_data.append({
                    "Lead Status": "NOT-ESCALATED",
                    "Agent Response": response
                })
            elif contains_budget == "No" and contains_scope == "Yes":
                missing_detail_prompt = generate_missing_detail_prompt("budget")
                response = generate_response(missing_detail_prompt, 400, 0.2)
                output_data.append({
                    "Lead Status": "NOT-ESCALATED",
                    "Agent Response": response
                })
            else:
                missing_detail_prompt = generate_missing_detail_prompt("scope")
                response = generate_response(missing_detail_prompt, 400, 0.2)
                output_data.append({
                    "Lead Status": "NOT-ESCALATED",
                    "Agent Response": response
                })

        # Save generated emails to CSV
        pd.DataFrame(output_data).to_csv(response_output_csv, index=False)
    except Exception as e:
        print(f"Error processing escalator agent: {e}")


if __name__ == "__main__":
    process_escalator_agent()