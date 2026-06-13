from flask import Flask, render_template, request, send_file, session, redirect, url_for, jsonify
import json
import re

from career_engine import analyze
from ai_career_advisor import generate_career_advice
from career_simulator import generate_simulation
from interview_coach import generate_interview_questions
from cv_generator import generate_cv
from cv_pdf import create_cv_pdf
from future_self_chat import ask_future_self

from career_momentum import add_momentum, get_momentum, get_level

app = Flask(__name__)
app.secret_key = "dev-secret-key"

chat_store = []
USE_AI = True


def _collect_contact_details(form):
    return {
        "name": form.get("name", "").strip(),
        "phone": form.get("phone", "").strip(),
        "email": form.get("email", "").strip(),
        "dob": form.get("dob", "").strip(),
    }


def _extract_company_name(text):
    if not text:
        return ""
    match = re.search(r"at\s+([^|\n]+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip(" -")
    return ""


def _collect_extra_cv_details(form):
    experience_entries = []
    if form.get("experience"):
        experience_entries.append(form.get("experience"))

    for index in range(50):
        company = form.get(f"exp_company_{index}", "").strip()
        role = form.get(f"exp_role_{index}", "").strip()
        dates = form.get(f"exp_dates_{index}", "").strip()
        details = form.get(f"exp_details_{index}", "").strip()

        if any([company, role, dates, details]):
            parts = []
            if role:
                parts.append(role)
            if company:
                parts.append(f"at {company}")
            if dates:
                parts.append(f"({dates})")
            if details:
                parts.append(details)
            experience_entries.append(" | ".join(parts))

    education_entries = []
    if form.get("education"):
        education_entries.append(form.get("education"))

    for index in range(50):
        degree = form.get(f"edu_degree_{index}", "").strip()
        institution = form.get(f"edu_institution_{index}", "").strip()
        year = form.get(f"edu_year_{index}", "").strip()

        if any([degree, institution, year]):
            parts = []
            if degree:
                parts.append(degree)
            if institution:
                parts.append(institution)
            if year:
                parts.append(year)
            education_entries.append(" | ".join(parts))

    return "\n\n".join(experience_entries), "\n\n".join(education_entries)


# -------------------------
# HOME
# -------------------------
@app.route('/')
def home():
    return render_template("index.html")


# -------------------------
# CAREER ANALYSIS
# -------------------------
@app.route('/analyze', methods=['POST'])
def analyze_career():
    session["chat_store"] = []

    skills_text = request.form['skills']
    target_role = request.form['role']
    current_role = request.form['current_role']


    simulation = generate_simulation(target_role)

    # AI OUTPUT
    if USE_AI:

        ai_output = generate_career_advice(
            current_role,
            skills_text,
            target_role
        )

        interview_questions = generate_interview_questions(target_role)

        try:
            ai_data = json.loads(ai_output)
        except:
            ai_data = {
                "hero_title": "Future Explorer",
                "power_level": 50,
                "rank": "Emerging Talent",
                "timeline": {
                    "today": "Starting journey...",
                    "3_months": "Learning foundations...",
                    "6_months": "Building experience...",
                    "12_months": "Career-ready phase..."
                },
                "future_paths": {
                    "safe_path": "",
                    "growth_path": "",
                    "bold_path": ""
                },
                "skill_quests": [],
                "boss_battles": [],
                "future_news_headline": "",
                "future_self_message": ai_output,
                "motivational_quote": ""
            }

    else:
        ai_data = {"future_self_message": "AI disabled"}
        interview_questions = []

    # -------------------------
    # CAREER SCORE
    # -------------------------
    result = analyze(
        skills_text.split(','),
        target_role
    )

    # -------------------------
    # MOMENTUM SYSTEM
    # -------------------------
    add_momentum(result["score"] * 4)

    # -------------------------
    # STORE SESSION
    # -------------------------
    session["latest_result"] = {
        "current_role": current_role,
        "target_role": target_role,
        "result": result,
        "ai_output": ai_data
    }

    return render_template(
        "result.html",
        result=result,
        role=target_role,
        current_role=current_role,
        simulation=simulation,
        ai=ai_data,
        interview_questions=interview_questions,
        momentum=get_momentum(),
        level=get_level(get_momentum())
    )


# -------------------------
# CV PAGE
# -------------------------
@app.route('/generate_cv', methods=["POST"])
def generate_cv_route():

    data = session.get("latest_result")

    if not data:
        return redirect(url_for("home"))

    extra_experience, extra_education = _collect_extra_cv_details(request.form)
    contact = _collect_contact_details(request.form)
    first_company = _extract_company_name(extra_experience) or request.form.get("exp_company_0", "").strip()

    cv_input = {
        "name": contact["name"] or data.get("current_role", ""),
        "phone": contact["phone"],
        "email": contact["email"],
        "dob": contact["dob"],
        "company": first_company,
        "current_role": request.form.get("current_role") or data["current_role"],
        "target_role": request.form.get("target_role") or data["target_role"],
        "skills": ",".join(data["result"]["matched"]),
        "experience": "\n\n".join(filter(None, [request.form.get("experience", ""), extra_experience])),
        "education": "\n\n".join(filter(None, [request.form.get("education", ""), extra_education])),
        "certifications": request.form.get("certifications", ""),
        "projects": request.form.get("projects", ""),
        "linkedin": request.form.get("linkedin", ""),
        "experience_years": request.form.get("experience_years", "")
    }

    cv = generate_cv(cv_input)
    cv.setdefault("contact", contact)
    session["last_cv"] = cv
    session["last_cv_input"] = cv_input
    add_momentum(25)

    chat_store.clear()
    session["chat_store"] = []

    return render_template(
        "cv.html",
        cv=cv,
        momentum=get_momentum(),
        level=get_level(get_momentum())
    )

@app.route('/cv_form')
def cv_form():
    return render_template("cv_form.html")

# -------------------------
# CHAT API
# -------------------------
@app.route('/api/future_chat', methods=['POST'])
def future_chat_api():

    data = request.json
    role = data['role']
    question = data['question']

    answer = ask_future_self(role, question)

    chat = session.get("chat_store", [])
    chat.append({"q": question, "a": answer})
    session["chat_store"] = chat

    return jsonify({"answer": answer})


@app.route('/api/interview_complete', methods=['POST'])
def interview_complete_api():
    add_momentum(40)
    return jsonify({"message": "Interview practice complete!", "momentum": get_momentum()})


@app.route('/interview_practice')
def interview_practice():
    data = session.get("latest_result")

    if not data:
        return redirect(url_for("home"))

    role = data.get("target_role", "your target role")
    questions_text = generate_interview_questions(role)
    session["interview_questions"] = questions_text

    return render_template("interview_practice.html", role=role, questions=questions_text, momentum=get_momentum(), level=get_level(get_momentum()))


@app.route('/download_cv')
def download_cv():
    data = session.get("latest_result")

    if not data:
        return redirect(url_for("home"))

    cv_input = session.get("last_cv_input") or {
        "name": "",
        "phone": "",
        "email": "",
        "dob": "",
        "current_role": data["current_role"],
        "target_role": data["target_role"],
        "skills": ",".join(data["result"]["matched"]),
        "experience": "",
        "education": "",
        "certifications": "",
        "projects": "",
        "linkedin": "",
        "experience_years": ""
    }

    cv = session.get("last_cv")

    if not cv:
        cv = generate_cv(cv_input)

    filename = "cv.pdf"
    create_cv_pdf(filename, cv)

    return send_file(filename, as_attachment=True)

# -------------------------
# CHAT PAGE
# -------------------------
@app.route('/future_chat_page')
def future_chat_page():

    chat = session.get("chat_store", [])

    return render_template(
        "future_chat.html",
        chat_history=chat,
        momentum=get_momentum(),
        level=get_level(get_momentum())
    )


# -------------------------
# BACK BUTTON FIX
# -------------------------
@app.route('/back_to_simulation')
def back_to_simulation():

    data = session.get("latest_result")

    if not data:
        return redirect(url_for("home"))

    return render_template(
        "result.html",
        result=data["result"],
        role=data["target_role"],
        current_role=data["current_role"],
        simulation=None,
        ai=data["ai_output"],
        momentum=get_momentum(),
        level=get_level(get_momentum())
    )


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)