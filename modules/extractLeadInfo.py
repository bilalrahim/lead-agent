from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load pre-trained T5 model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


def ExtractLeadInfo(lead_data):
    """
    Extract industry and needs information from lead data using T5 model.

    Parameters:
    - lead_data (str): Lead data to extract information from.

    Returns:
    dict: Dictionary containing extracted information with keys 'industry' and 'needs'.
          Returns None in case of an error during extraction.
    """
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
    """
    Extract information using T5 model and tokenizer.

    Parameters:
    - model: T5 model.
    - tokenizer: T5 tokenizer.
    - prompt (str): Prompt for extraction.

    Returns:
    str: Extracted information.
    Raises an exception in case of an error during extraction.
    """
    try:
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model(**inputs, decoder_input_ids=inputs["input_ids"])
        decoded_output = tokenizer.decode(outputs['logits'].argmax(dim=-1).squeeze().tolist(), skip_special_tokens=True)
        return decoded_output
    except Exception as e:
        print(f"Error during T5 extraction: {e}")
        raise


if __name__ == "__main__":
    # Example usage when running the script directly
    lead_data = "Sample lead data"
    extracted_info = ExtractLeadInfo(lead_data)
    if extracted_info:
        # Process extracted information as needed
        print("Processed extracted info:", extracted_info)