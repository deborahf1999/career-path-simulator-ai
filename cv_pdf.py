from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item)
    return str(value)


def create_cv_pdf(filename, cv):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    contact = cv.get("contact") if isinstance(cv.get("contact"), dict) else {}
    name = cv.get("name") or contact.get("name") or "AI Generated Resume"
    phone = cv.get("phone") or contact.get("phone") or ""
    email = cv.get("email") or contact.get("email") or ""
    dob = cv.get("dob") or contact.get("dob") or ""

    content.append(Paragraph(name, styles["Title"]))
    details = [item for item in [phone, email, dob] if item]
    if details:
        content.append(Paragraph(" | ".join(details), styles["BodyText"]))
    content.append(Spacer(1, 12))

    if cv.get("summary"):
        content.append(Paragraph(cv["summary"], styles["BodyText"]))
        content.append(Spacer(1, 12))

    if cv.get("skills"):
        content.append(Paragraph("Skills", styles["Heading2"]))
        for skill in cv["skills"]:
            content.append(Paragraph(f"• {skill}", styles["BodyText"]))
        content.append(Spacer(1, 12))

    if cv.get("experience"):
        content.append(Paragraph("Experience", styles["Heading2"]))
        for exp in cv["experience"]:
            title = exp.get("title") or exp.get("role") or "Experience"
            company = exp.get("company") or ""
            duration = exp.get("duration") or ""
            content.append(Paragraph(title, styles["Heading3"]))
            if company:
                content.append(Paragraph(company, styles["BodyText"]))
            if duration:
                content.append(Paragraph(duration, styles["BodyText"]))
            for item in exp.get("responsibilities", []) or []:
                content.append(Paragraph(f"• {item}", styles["BodyText"]))
            content.append(Spacer(1, 6))
        content.append(Spacer(1, 12))

    if cv.get("projects"):
        content.append(Paragraph("Projects", styles["Heading2"]))
        for project in cv["projects"]:
            if isinstance(project, dict):
                name = project.get("name") or "Project"
                description = project.get("description") or project.get("details") or ""
            else:
                name = str(project)
                description = ""
            content.append(Paragraph(name, styles["Heading3"]))
            if description:
                content.append(Paragraph(description, styles["BodyText"]))
        content.append(Spacer(1, 12))

    if cv.get("education"):
        content.append(Paragraph("Education", styles["Heading2"]))
        for edu in cv["education"]:
            degree = edu.get("degree") or ""
            institution = edu.get("institution") or ""
            year = edu.get("year_completed") or ""
            if degree:
                content.append(Paragraph(degree, styles["Heading3"]))
            if institution:
                content.append(Paragraph(institution, styles["BodyText"]))
            if year:
                content.append(Paragraph(year, styles["BodyText"]))
            content.append(Spacer(1, 6))
        content.append(Spacer(1, 12))

    if cv.get("certifications"):
        content.append(Paragraph("Certifications", styles["Heading2"]))
        for cert in cv["certifications"]:
            if isinstance(cert, dict):
                text = cert.get("name") or "Certification"
            else:
                text = str(cert)
            content.append(Paragraph(f"• {text}", styles["BodyText"]))
        content.append(Spacer(1, 12))

    doc.build(content)