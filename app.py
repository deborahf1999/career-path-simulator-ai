from career_simulator import generate_simulation
from flask import Flask, render_template, request
from career_engine import analyze
from ai_career_advisor import generate_career_advice
from flask import send_file
from pdf_generator import create_career_pdf
from interview_coach import generate_interview_questions

app = Flask(__name__)
latest_result = {}
USE_AI = True

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze_career():

    skills_text = request.form['skills']
    target_role = request.form['role']
    simulation = generate_simulation(target_role)
    current_role = request.form['current_role']
    global latest_result
 

    if USE_AI:
        ai_output = generate_career_advice(
            current_role,
            skills_text,
            target_role
        )

        interview_questions = generate_interview_questions(
            target_role
        )
    else:
        ai_output = """
    AI Career Coach disabled in development mode.
    """
        interview_questions = "Interview mode disabled."

    user_skills = skills_text.split(',')

    result = analyze(
        user_skills,
        target_role
    )

    if result["score"] < 40:
        readiness = "Beginner"

    elif result["score"] < 70:
        readiness = "Emerging"

    elif result["score"] < 90:
        readiness = "Career Ready"

    else:
        readiness = "Expert Ready"

    if result["score"] >= 80:
        success_rate = 90
        timeline = "1-3 Months"
        difficulty = "Easy"

    elif result["score"] >= 60:
        success_rate = 75
        timeline = "3-6 Months"
        difficulty = "Medium"

    elif result["score"] >= 40:
        success_rate = 60
        timeline = "6-9 Months"
        difficulty = "Medium"

    else:
        success_rate = 40
        timeline = "9-12 Months"
        difficulty = "Hard"

    latest_result = {
        "current_role": current_role,
        "target_role": target_role,
        "result": result,
        "ai_output": ai_output
    }
        
    return render_template(
        "result.html",
        result=result,
        role=target_role,
        current_role=current_role,
        simulation=simulation,
        ai_output=ai_output,
        readiness=readiness,
        interview_questions=interview_questions,
        success_rate=success_rate,
        timeline=timeline,
        difficulty=difficulty,
    )

@app.route('/download')
def download_report():

    filename = "career_report.pdf"

    create_career_pdf(
        filename,
        latest_result["current_role"],
        latest_result["target_role"],
        latest_result["result"],
        latest_result["ai_output"]
    )

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)