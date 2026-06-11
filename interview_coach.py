from openai import AzureOpenAI
import os


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def generate_interview_questions(role):

    prompt = f"""
Generate interview preparation questions for a {role}.

Create:

1. Five technical questions
2. Three behavioral questions
3. Two scenario-based questions

Format clearly.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content