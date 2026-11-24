"""Reads a resume (.pdf or .txt) and finds the skills mentioned in it."""
import re

# skill word -> quiz category it belongs to
SKILLS = {
    "python": "Python", "django": "Flask", "flask": "Flask", "fastapi": "Flask",
    "jinja": "Flask", "html": "HTML & CSS", "css": "HTML & CSS",
    "bootstrap": "HTML & CSS", "tailwind": "HTML & CSS", "javascript": "HTML & CSS",
    "react": "HTML & CSS", "sql": "SQL & Databases", "postgresql": "SQL & Databases",
    "postgres": "SQL & Databases", "mysql": "SQL & Databases", "sqlite": "SQL & Databases",
    "mongodb": "SQL & Databases", "sqlalchemy": "SQL & Databases", "git": "Git & Web",
    "github": "Git & Web", "rest": "Git & Web", "api": "Git & Web", "json": "Git & Web",
    "docker": "Git & Web", "algorithms": "DSA & CS", "data structures": "DSA & CS",
    "dsa": "DSA & CS", "java": "DSA & CS", "c++": "DSA & CS",
}


def extract_text(path):
    """Return the plain text of a .pdf or .txt file ('' if nothing readable)."""
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(pages).strip()
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read().strip()


def find_skills(text):
    """Return the list of known skills that appear in the text."""
    lowered = text.lower()
    found = []
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9+])" + re.escape(skill) + r"(?![a-z0-9+])", lowered):
            found.append(skill)
    return found


def categories_for(skills):
    """Quiz categories that match the skills found in a resume."""
    return sorted({SKILLS[s] for s in skills})
