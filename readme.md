# Opener and Escalator Agent using LLM's

## Description
This project consists of two essential components: Opener and Escalator.

### Opener
The Opener script serves to streamline the initial interaction with potential leads. Leveraging lead information, it autonomously drafts personalized emails introducing your software firm and eliciting further details. Opener utilizes Cohere's LLM (Language Model) technology to craft compelling email subjects and bodies.

- Opener saves prompts in the `opener_prompts.md` file and email subject-body pairs in `opener_output.csv`.

### Escalator
The Escalator Agent, on the other hand, functions as a responsive mechanism post-email deployment. It gauges lead responses and, based on their content, decides whether to escalate the lead for further engagement or prompt for additional information. Escalator employs Cohere's chat API to extract crucial information from lead responses and Cohere's generate API to compose follow-up messages if necessary.

- Escalator saves prompts in the `escalator_prompts.md` file and lead status along with responses in `escalator_output.csv`.

## Integration with Cohere
- **Opener:** Utilizes [Cohere's Generate API](https://python.langchain.com/docs/integrations/providers/cohere#llm) for email subject-body generation.
- **Escalator:** Leverages [Cohere's Chat API](https://python.langchain.com/docs/integrations/providers/cohere#chat) for lead response analysis and the generate API for response generation.


## Installation Instructions
### Python Version: 3.10.9
1. Install required packages using the `requirements.txt` file.
2. Add your Cohere API key to the `.env` file.
3. Run the following commands in your terminal (please wait for the execution of the first cmd):
   ```bash
   python opener.agent.py
   python escalator.agent.py

## Future Improvements
1. Build a user interface (UI) where the sales team can upload a CSV containing leads and view/respond to corresponding responses.

2. Deploy the scripts to a serverless environment, preferably Firebase Cloud Functions, to utilize the free tier for hosting.

## Side Note:
When running escalator.agent.py you may get error that Cohere free tier limit reached but it does complete the execuation of all the leads.
