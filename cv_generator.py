from openai import AzureOpenAI
import os
import json
import re

api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

client = None
if api_key and azure_endpoint:
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2024-12-01-preview",
        azure_endpoint=azure_endpoint
    )

DEFAULT_CV = {
    "summary": "Professional candidate with strong technical and problem-solving skills.",
    "skills": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "education": [],
    "advantages": []
}


def _extract_json_object(text):
    if not text:
        return None

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.rstrip("`").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else None


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_skills(value):
    skills = []
    for item in _as_list(value):
        if isinstance(item, dict):
            skill = item.get("name") or item.get("skill") or item.get("title")
        else:
            skill = str(item)
        if isinstance(skill, str) and skill.strip():
            skills.append(skill.strip())
    return skills


def _normalize_experience(value):
    normalized = []
    for item in _as_list(value):
        if isinstance(item, dict):
            responsibilities = item.get("responsibilities") or item.get("details") or item.get("description") or []
            if isinstance(responsibilities, str):
                responsibilities = [responsibilities]
            elif not isinstance(responsibilities, list):
                responsibilities = [str(responsibilities)] if responsibilities else []

            normalized.append({
                "title": item.get("title") or item.get("role") or item.get("position") or "Experience",
                "company": item.get("company") or item.get("organization") or "",
                "duration": item.get("duration") or item.get("period") or "",
                "responsibilities": responsibilities
            })
        else:
            normalized.append({
                "title": str(item),
                "company": "",
                "duration": "",
                "responsibilities": []
            })
    return normalized


def _normalize_projects(value):
    normalized = []
    for item in _as_list(value):
        if isinstance(item, dict):
            name = item.get("name") or item.get("title") or item.get("project") or "Project"
            description = item.get("description") or item.get("details") or item.get("summary") or ""
            normalized.append({"name": name, "description": description})
        else:
            normalized.append({"name": str(item), "description": ""})
    return normalized


def _normalize_certifications(value):
    normalized = []
    for item in _as_list(value):
        if isinstance(item, dict):
            name = item.get("name") or item.get("title") or item.get("certificate") or "Certification"
            normalized.append({"name": name})
        else:
            text = str(item).strip()
            if text:
                normalized.append({"name": text})
    return normalized


def _normalize_education(value):
    normalized = []
    for item in _as_list(value):
        if isinstance(item, dict):
            normalized.append({
                "degree": item.get("degree") or item.get("qualification") or "",
                "institution": item.get("institution") or item.get("school") or "",
                "year_completed": item.get("year_completed") or item.get("year") or ""
            })
        else:
            normalized.append({"degree": "", "institution": str(item), "year_completed": ""})
    return normalized


def _normalize_advantages(value):
    advantages = []
    for item in _as_list(value):
        text = item.get("name") if isinstance(item, dict) else str(item)
        if isinstance(text, str) and text.strip():
            advantages.append(text.strip())
    return advantages


def _parse_experience_blocks(value):
    blocks = [block.strip() for block in str(value).split("\n\n") if block.strip()]
    parsed = []

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue

        title = lines[0]
        company = ""
        duration = ""
        responsibilities = []

        if " | " in block:
            parts = [part.strip() for part in block.split(" | ")]
            title = parts[0] if parts else title
            if len(parts) > 1:
                company = parts[1].replace("at ", "", 1) if parts[1].startswith("at ") else parts[1]
            if len(parts) > 2:
                duration = parts[2].strip("()") if parts[2].startswith("(") and parts[2].endswith(")") else parts[2]
            if len(parts) > 3:
                responsibilities = [parts[3]]
        else:
            if len(lines) > 1:
                responsibilities = lines[1:]

        parsed.append({
            "title": title,
            "company": company,
            "duration": duration,
            "responsibilities": responsibilities or ["Applied professional skills and delivered results in a real work setting."]
        })

    return parsed


def _normalize_cv(cv, data):
    if not isinstance(cv, dict):
        cv = {}

    skills = _normalize_skills(cv.get("skills", data.get("skills", "")))
    if not skills:
        skills = [item.strip() for item in str(data.get("skills", "")).split(",") if item.strip()]

    experience = _normalize_experience(cv.get("experience", []))
    if not experience:
        parsed = _parse_experience_blocks(data.get("experience", ""))
        if parsed:
            experience = parsed
        else:
            role = data.get("current_role", "Professional") or "Professional"
            experience = [{
                "title": role,
                "company": data.get("company") or "Professional Experience",
                "duration": data.get("experience_years", "3+ years") or "3+ years",
                "responsibilities": [
                    "Delivered dependable work and contributed to team goals in a professional setting.",
                    "Applied communication, problem solving, and continuous learning to support meaningful impact."
                ]
            }]

    projects = _normalize_projects(cv.get("projects", []))
    if not projects and data.get("projects"):
        projects = [{"name": "Portfolio project", "description": data.get("projects")}]

    certifications = _normalize_certifications(cv.get("certifications", []))
    if not certifications and data.get("certifications"):
        certifications = [{"name": item.strip()} for item in str(data.get("certifications", "")).split("\n") if item.strip()]

    education = _normalize_education(cv.get("education", []))
    if not education and data.get("education"):
        education = [{"degree": "", "institution": data.get("education"), "year_completed": ""}]

    advantages = []

    contact = {
        "name": data.get("name") or "",
        "phone": data.get("phone") or "",
        "email": data.get("email") or "",
        "dob": data.get("dob") or "",
    }

    summary = cv.get("summary") or f"{data.get('current_role', 'Professional')} candidate with strong skills in {', '.join(skills[:6]) or 'core technologies'}."

    return {
        "summary": summary,
        "skills": skills or DEFAULT_CV["skills"],
        "experience": experience or DEFAULT_CV["experience"],
        "projects": projects or DEFAULT_CV["projects"],
        "certifications": certifications or DEFAULT_CV["certifications"],
        "education": education or DEFAULT_CV["education"],
        "advantages": advantages,
        "contact": contact,
        "name": contact["name"],
        "phone": contact["phone"],
        "email": contact["email"],
        "dob": contact["dob"]
    }


def _build_fallback_cv(data):
    skills_list = [item.strip() for item in str(data.get("skills", "")).split(",") if item.strip()]

    role = data.get("current_role", "Professional") or "Professional"
    target = data.get("target_role", "Career Growth") or "Career Growth"
    summary = (
        f"Dedicated {role} with strong foundational experience in {', '.join(skills_list[:5]) or 'core professional skills'} "
        f"and a clear goal of transitioning into {target}. "
        "Brings problem-solving, communication, adaptability, and a growth mindset to deliver reliable results and contribute to modern teams."
    )

    extra_skills = [
        "Project Delivery",
        "Adaptability",
        "Team Collaboration",
        "Stakeholder Communication",
        "Continuous Learning"
    ]
    skills = list(dict.fromkeys((skills_list + extra_skills)[:16]))

    experience_blocks = [block.strip() for block in str(data.get("experience", "")).split("\n\n") if block.strip()]
    experience = []
    if not experience_blocks:
        experience = [
            {
                "title": role,
                "company": data.get("company") or "Professional Experience",
                "duration": data.get("experience_years", "3+ years") or "3+ years",
                "responsibilities": [
                    f"Applied core skills in {', '.join(skills_list[:4]) or 'professional work'} to deliver reliable results.",
                    "Contributed to team collaboration, continuous improvement, and problem solving.",
                    "Prepared for growth into " + target + " with a strong professional foundation."
                ]
            }
        ]

    for block in experience_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        title = data.get("current_role", "Professional")
        company = ""
        duration = data.get("experience_years", "")
        responsibilities = lines

        if " | " in block:
            parts = [part.strip() for part in block.split(" | ")]
            title = parts[0] if parts else title
            if len(parts) > 1:
                company = parts[1].replace("at ", "", 1) if parts[1].startswith("at ") else parts[1]
            if len(parts) > 2:
                duration = parts[2]
            if len(parts) > 3:
                responsibilities = [parts[3]]

        experience.append({
            "title": title,
            "company": company,
            "duration": duration or "Experience",
            "responsibilities": responsibilities
        })

    if not experience and (data.get("experience") or data.get("experience_years")):
        experience = _parse_experience_blocks(data.get("experience", ""))
        if not experience:
            experience = [{
                "title": data.get("current_role", "Professional") or "Professional Experience",
                "company": data.get("company") or "Professional Experience",
                "duration": data.get("experience_years", "0+ years") or "0+ years",
                "responsibilities": [data.get("experience") or "Experience details to be added in the final resume."]
            }]

    education_blocks = [block.strip() for block in str(data.get("education", "")).split("\n\n") if block.strip()]
    education = []
    for block in education_blocks:
        if " | " in block:
            parts = [part.strip() for part in block.split(" | ")]
            degree = parts[0] if parts else ""
            institution = parts[1] if len(parts) > 1 else ""
            year = parts[2] if len(parts) > 2 else ""
        else:
            degree = ""
            institution = block
            year = ""

        education.append({
            "degree": degree,
            "institution": institution,
            "year_completed": year
        })

    if not education:
        education = [{
            "degree": "Degree / Certification Details",
            "institution": data.get("education") or "Education details to be added in the final resume.",
            "year_completed": "Current"
        }]

    projects_list = []
    if data.get("projects"):
        projects_list.append({"name": "Project / Achievement", "description": data.get("projects")})
    projects_list.extend([
        {"name": "Career Growth Project", "description": f"Prepared for a transition into {target} by strengthening relevant technical and professional skills."},
        {"name": "Professional Development", "description": "Built confidence in communication, problem solving, and adaptability for real-world work environments."}
    ])

    contact = {
        "name": data.get("name") or "",
        "phone": data.get("phone") or "",
        "email": data.get("email") or "",
        "dob": data.get("dob") or "",
    }

    return {
        "summary": summary,
        "skills": skills or DEFAULT_CV["skills"],
        "experience": experience or DEFAULT_CV["experience"],
        "projects": projects_list if projects_list else DEFAULT_CV["projects"],
        "certifications": [
            {"name": item.strip()} for item in str(data.get("certifications", "")).split("\n") if item.strip()
        ] or DEFAULT_CV["certifications"],
        "education": education or DEFAULT_CV["education"],
        "advantages": DEFAULT_CV["advantages"],
        "contact": contact,
        "name": contact["name"],
        "phone": contact["phone"],
        "email": contact["email"],
        "dob": contact["dob"]
    }


def generate_cv(data):
    if client is None:
        return _build_fallback_cv(data)

    prompt = f"""
Create a professional ATS-friendly resume.

Return ONLY valid JSON for a professional CV/resume.
Do not include an 'advantages' section.
Use a clean, ATS-friendly layout.

Format:
{{
  "summary": "",
  "skills": [],
  "experience": [],
  "projects": [],
  "certifications": [],
  "education": []
}}

INPUT:
{json.dumps(data)}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw_content = getattr(response.choices[0].message, "content", "")
        cv = _extract_json_object(raw_content)

        if isinstance(cv, dict):
            return _normalize_cv(cv, data)
    except Exception:
        pass

    return _normalize_cv(_build_fallback_cv(data), data)