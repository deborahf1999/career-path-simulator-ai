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
    You are a cinematic career simulation AI.

    Return ONLY valid JSON. No markdown.

    CRITICAL FORMATTING RULES:
    - Always use proper English sentences
    - Always include spaces between words
    - Never merge words together
    - Use readable human-style writing
    - Each sentence must be clear and spaced properly

    Current Role: {current_role}
    Skills: {skills}
    Target Role: {target_role}

    Return EXACT JSON:

    {{
    "hero_title": "",
    "power_level": 0,
    "rank": "",
    
    "career_readiness_score": 0,
    "career_probability": "",

    "transferable_skills": [],
    "skill_gaps": [],
    "recommended_learning_path": [],

    "timeline": {{
        "today": "",
        "3_months": "",
        "6_months": "",
        "12_months": ""
    }},

    "future_paths": {{
        "safe_path": "",
        "growth_path": "",
        "bold_path": ""
    }},

    "skill_quests": [],
    "boss_battles": [],
    "future_news_headline": "",
    "future_self_message": "",
    "motivational_quote": ""
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=800
    )


    return response.choices[0].message.content