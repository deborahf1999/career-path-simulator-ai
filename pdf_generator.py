from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_career_pdf(
    filename,
    current_role,
    target_role,
    result,
    ai_output
):
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Career Path Simulator AI Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"Current Role: {current_role}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Target Role: {target_role}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Match Score: {result['score']}%", styles["Normal"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Matched Skills: " + ", ".join(result["matched"]),
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Missing Skills: " + ", ".join(result["missing"]),
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph("AI Career Coach Advice", styles["Heading2"])
    )

    content.append(
        Paragraph(ai_output.replace("\n", "<br/>"), styles["Normal"])
    )

    doc.build(content)