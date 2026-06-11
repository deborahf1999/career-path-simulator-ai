import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def generate_career_advice(current_role, skills, target_role):

    prompt = f"""
    Current Role: {current_role}

    Current Skills:
    {skills}

    Target Role:
    {target_role}

    Generate:

    1. Career Summary
    2. Skills to Learn
    3. Recommended Certifications
    4. 6 Month Learning Roadmap
    5. Career Advice

    Keep it concise and practical.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content