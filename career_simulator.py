def generate_simulation(role):

    role = role.lower().strip()

    return {
        "avatar": f"{role.title()} Explorer",
        "quests": [
            f"Learn fundamentals of {role}",
            f"Understand industry tools used in {role}",
            f"Build 2–3 real-world projects in {role}"
        ],
        "future": [
            f"Entry-level {role}",
            f"Mid-level {role}",
            f"Senior {role} / Specialist"
        ]
    }