from flask import session

def get_level(momentum):

    if momentum < 50:
        return "Level 1 - Explorer"
    elif momentum < 120:
        return "Level 2 - Learner"
    elif momentum < 250:
        return "Level 3 - Practitioner"
    elif momentum < 400:
        return "Level 4 - Professional"
    else:
        return "Level 5 - Master"


def add_momentum(points):

    current = session.get("momentum", 0)
    current += points
    session["momentum"] = current

    return current


def get_momentum():
    return session.get("momentum", 0)