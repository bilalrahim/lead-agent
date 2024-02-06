# Opener and Escalator Agent using LLM's

## Description
This project comprises two scripts: Opener and Escalator Agent. The Opener script utilizes Cohere's LLM (Language Model) to generate an introductory email to leads, introducing your software firm and requesting further details. On the other hand, the Escalator Agent, based on the lead's response to the email, either escalates the lead for further action or sends another response requesting additional information. The Opener script creates an `opener_prompts.md` file to save prompts and an `opener_output.csv` file to save the email subject and body. Similarly, the Escalator Agent creates an `escalator_prompts.md` file for prompts and an `escalator_output.csv` file for status and responses.

## Installation Instructions
1. Install required packages using the `requirements.txt` file.
2. Add your Cohere API key to the `.env` file.
3. Run the following commands in your terminal:
   ```bash
   python opener.agent.py
   python escalator.agent.py

## Future Improvements
1. Build a user interface (UI) where the sales team can upload a CSV containing leads and view/respond to corresponding responses.

2. Deploy the scripts to a serverless environment, preferably Firebase Cloud Functions, to utilize the free tier for hosting.

## Side Note:
When running escalator.agent.py you may get error that Cohere free tier limit reached but it does complete the execuation of all the leads.