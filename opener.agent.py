import pandas as pd
# from langchain_openai import OpenAI
from langchain.prompts.prompt import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# For prompt engineering.
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

openai_api_key = "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"

input_csv = "leads.csv"
prompt_output_file = "prompts.txt"
email_output_csv = "opener_output.csv"

# Function to extract key information from lead data using T5.
def extract_lead_info(lead_data):
    print(f'Extracting information from lead data: {lead_data}')
    prompt_industry = f"Extract the industry from the lead data: {lead_data}"
    prompt_needs = f"Extract the needs of the company from the lead data: {lead_data}"

    try:
        # Extract information using T5.
        extracted_info = {
            "industry": extract_from_t5(model, tokenizer, prompt_industry),
            "needs": extract_from_t5(model, tokenizer, prompt_needs)
        }
        print("Extracted info:", extracted_info)
        return extracted_info
    except Exception as e:
        print(f"Error extracting information: {e}")
        return None

def extract_from_t5(model, tokenizer, prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model(**inputs, decoder_input_ids=inputs["input_ids"])
        decoded_output = tokenizer.decode(outputs['logits'].argmax(dim=-1).squeeze().tolist(), skip_special_tokens=True)
        return decoded_output
    except Exception as e:
        print(f"Error during T5 extraction: {e}")
        raise

# Function to generate a personalized prompt based on extracted information
def generate_prompt(lead_info):
    template = """
            Antematter is a software consultancy provider that specializes 
            in helping businesses optimize their digital operations and achieve their goals.
            {antematter_description}
            Write a cold email introducing Antematter 
            to {lead_name}, of {company_name}, a {industry} company with {company_size} employees, 
            and inquire about their potential need for {needs}. 
            Please keep the tone professional and engaging.
          """
    prompt_template = PromptTemplate(
        template = template,
        input_variables = [
            "antematter_description",
            "lead_name",
            "company_name",
            "industry",
            "company_size",
            "needs"
            ]
    )

    return prompt_template.format(antematter_description=lead_info["antematter_description"], 
                           lead_name=lead_info["lead_name"], company_name=lead_info["company_name"], 
                           industry=lead_info["industry"], company_size=lead_info["company_size"], 
                           needs=lead_info["needs"])
def generate_opener_email(prompt):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

    try:
        # Generate email subject (limited to 30 characters)
        response = llm(prompt + " Subject:", max_tokens=30)  # Limit response length
        subject = response.strip().capitalize()

        # Generate email body (limited to 150 tokens, approximately 3 paragraphs)
        response = llm(prompt + "\n\nBody:", max_tokens=150)
        body = response.strip()

        return subject, body
    except Exception as e:
        print(f"Error during T5 extraction: {e}")
        raise

def process_opener_agent():
    output_data = []
    df = pd.read_csv(input_csv)
    for index, row in df.iterrows():
        print(f"Processing lead {index + 1} of {len(df)}")
        lead = row.to_dict()

        # Extract lead information.
        try:
            lead_requirements = extract_lead_info(lead['Looking For'])
        except KeyError:
            print(f"Missing information in lead: {lead['Name']}")
            continue

        # Generate Personalized Prompt.
        print(f"Generating prompt for {lead['Name']}")
        prompt_info = {
            **lead_requirements,
            "antematter_description": "Antematter develops and improves cutting-edge solutions using Blockchain & AI with one guarantee: maximum performance, in every sense of the word.",
            "lead_name": lead['Name'],
            "company_name": lead['Organizaton'],
            "company_size": lead['Company Size'],
        }
        prompt = generate_prompt(prompt_info)

        # Save prompt to a file.
        with open(prompt_output_file, "w") as f:
            f.write(prompt)
        subject, body = generate_opener_email(prompt)

        output_data.append({
            "Email Subject": subject,
            "Email Body": body,
        })

    # Save generated emails to CSV
    pd.DataFrame(output_data).to_csv(email_output_csv, index=False)

process_opener_agent()