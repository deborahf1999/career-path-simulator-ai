from openai import AzureOpenAI
import os
import re


client = None
if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def _fallback_questions(role):
    return [
        f"Tell me about yourself and why you want to work as a {role}.",
        f"Describe a time you solved a difficult problem in your {role} work.",
        "What skills do you bring that make you a strong fit for this role?",
        "How do you handle tight deadlines or changing priorities?",
        "Tell me about a project you are proud of and the result you achieved.",
        "How do you collaborate with teammates or stakeholders?",
        "What is one lesson you learned from a recent challenge?",
        "How would you explain your experience to a hiring manager in this field?"
    ]


def generate_interview_questions(role):

    prompt = f"""
Generate interview preparation questions for a {role}.

Create:

1. Five technical questions
2. Three behavioral questions
3. Two scenario-based questions

Format clearly.
"""

    if client is None:
        return _fallback_questions(role)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        text = getattr(response.choices[0].message, "content", "") or ""
        lines = []
        for raw in text.splitlines():
            line = raw.strip()
            line = re.sub(r"^\s*(?:[-*\d\.]+\s*)+", "", line)
            line = line.strip(" •-")
            if not line:
                continue
            if line.lower().startswith("here are") or line.lower().startswith("certainly"):
                continue
            if re.search(r"\b(technical|behavioral|scenario|questions)\b", line, flags=re.IGNORECASE) and len(line.split()) <= 4:
                continue
            lines.append(line)

        cleaned = [line for line in lines if line.endswith("?") or line.endswith(".")]
        if cleaned:
            return cleaned[:10]
    except Exception:
        pass

    return _fallback_questions(role)