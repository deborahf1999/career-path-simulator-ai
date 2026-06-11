from skill_data import CAREERS

def generate_badges(score):

    badges = []

    if score >= 20:
        badges.append("🏅 Career Explorer")

    if score >= 40:
        badges.append("🥈 Skill Builder")

    if score >= 60:
        badges.append("🥇 Career Specialist")

    if score >= 80:
        badges.append("💎 Future Expert")

    return badges

def analyze(user_skills, target_role):

    required_skills = CAREERS[target_role]["skills"]

    matched = []

    for skill in required_skills:
        if skill.lower() in [s.strip().lower() for s in user_skills]:
            matched.append(skill)

    missing = [
        skill
        for skill in required_skills
        if skill not in matched
    ]

    score = int(
        len(matched) /
        len(required_skills)
        * 100
    )

    if score <= 20:
        level = "Level 1 - Explorer"

    elif score <= 40:
        level = "Level 2 - Builder"

    elif score <= 60:
        level = "Level 3 - Specialist"

    elif score <= 80:
        level = "Level 4 - Professional"

    else:
        level = "Level 5 - Expert"

    badges = generate_badges(score)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "level": level,
        "badges": badges
    }