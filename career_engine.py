from openai import AzureOpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def analyze(user_skills, target_role):

    prompt = f"""
    Evaluate this career transition.

    Skills:
    {', '.join(user_skills)}

    Target Role:
    {target_role}

    Return JSON:

    {{
      "score": 0,
      "level": "",
      "matched": [],
      "missing": [],
      "badges": []
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        response_format={"type": "json_object"}
    )

    return json.loads(
        response.choices[0].message.content
    )