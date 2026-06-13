import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def ai_score_answer(text):

    prompt = f"""
    Score this answer from 1 to 10 based on career quality:

    Answer:
    {text}

    Return only a number.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return int(response.choices[0].message.content.strip())
    except:
        return 5