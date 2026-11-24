"""ATS (Applicant Tracking System) score for a resume.

How the 100 points are split:
  Keyword match      35   (role keywords, or the job description if you paste one)
  Resume sections    20   (summary, education, experience, skills, projects, certifications)
  Contact details    10   (email, phone, LinkedIn/GitHub)
  Content quality    20   (action verbs, numbers/results, bullet points)
  Length & format    15   (a sensible word count, readable text)
"""
import re

ROLE_KEYWORDS = {
    "backend": ["python", "flask", "django", "api", "rest", "sql", "postgresql", "database",
                "git", "docker", "authentication", "sqlalchemy", "json", "testing", "linux"],
    "frontend": ["html", "css", "javascript", "react", "responsive", "git", "api", "bootstrap",
                 "accessibility", "typescript", "figma", "flexbox", "ui", "testing"],
    "full stack": ["html", "css", "javascript", "python", "flask", "react", "sql", "api",
                   "git", "database", "docker", "rest", "deployment", "testing"],
    "data": ["python", "sql", "excel", "pandas", "numpy", "visualization", "statistics",
             "tableau", "power bi", "analysis", "dashboard", "machine learning", "reporting"],
    "devops": ["linux", "docker", "kubernetes", "ci/cd", "aws", "git", "monitoring",
               "terraform", "automation", "bash", "jenkins", "cloud"],
    "general": ["python", "java", "sql", "git", "api", "algorithms", "data structures",
                "testing", "problem solving", "teamwork", "communication", "projects"],
}

SECTIONS = {
    "Summary / objective": ["summary", "objective", "profile", "about me"],
    "Education": ["education", "academic", "qualification", "university", "college", "b.tech", "bachelor"],
    "Experience / internship": ["experience", "internship", "employment", "work history"],
    "Skills": ["skills", "technologies", "technical skills", "tech stack"],
    "Projects": ["projects", "project work", "personal projects"],
    "Certifications / achievements": ["certification", "certifications", "achievements", "awards", "courses"],
}

ACTION_VERBS = ["built", "developed", "designed", "created", "implemented", "led", "managed",
                "improved", "optimized", "optimised", "launched", "automated", "analyzed",
                "analysed", "deployed", "integrated", "reduced", "increased", "delivered",
                "collaborated", "tested", "maintained", "wrote", "migrated"]

STOP_WORDS = set("""the and for with that this from have has are was were will you your our their
they them his her its into over under about more than such other also can may must should would
could been being who whom what when where which while who job role work team experience years
year required preferred strong ability skills knowledge good great including etc using use used
looking join company candidate responsibilities requirements""".split())


def _pick_keywords(role, job_description):
    """Return (keywords, source_label)."""
    if job_description.strip():
        words = re.findall(r"[a-zA-Z][a-zA-Z+#./-]{2,}", job_description.lower())
        counts = {}
        for word in words:
            if word not in STOP_WORDS:
                counts[word] = counts.get(word, 0) + 1
        top = sorted(counts, key=lambda w: (-counts[w], w))[:20]
        if len(top) >= 5:
            return top, "your job description"
    lowered = role.lower()
    for key in ("full stack", "backend", "frontend", "devops", "data"):
        if key in lowered or (key == "backend" and ("python" in lowered or "flask" in lowered)):
            return ROLE_KEYWORDS[key], f"the {role or key} role"
    if "web" in lowered or "developer" in lowered:
        return ROLE_KEYWORDS["full stack"], f"the {role} role"
    return ROLE_KEYWORDS["general"], "a general software role"


def _has(text, word):
    return re.search(r"(?<![a-z0-9+])" + re.escape(word) + r"(?![a-z0-9+])", text) is not None


def analyze(text, role="", job_description=""):
    """Return a dict with the total score, a breakdown and suggestions."""
    lowered = text.lower()
    words = re.findall(r"[A-Za-z0-9+#./-]+", text)
    word_count = len(words)
    breakdown, tips = [], []

    # ---- 1. keywords (35) ----
    keywords, source = _pick_keywords(role, job_description)
    matched = [k for k in keywords if _has(lowered, k)]
    missing = [k for k in keywords if k not in matched]
    kw_points = round(35 * len(matched) / len(keywords))
    breakdown.append({"label": "Keyword match", "got": kw_points, "max": 35,
                      "note": f"{len(matched)} of {len(keywords)} keywords for {source}"})
    if missing:
        tips.append("Add the missing keywords that are true for you, for example: " + ", ".join(missing[:6]) + ".")

    # ---- 2. sections (20) ----
    found_sections = {name: any(_has(lowered, h) for h in heads) for name, heads in SECTIONS.items()}
    sec_points = round(20 * sum(found_sections.values()) / len(SECTIONS))
    breakdown.append({"label": "Resume sections", "got": sec_points, "max": 20,
                      "note": f"{sum(found_sections.values())} of {len(SECTIONS)} standard sections found"})
    for name, ok in found_sections.items():
        if not ok:
            tips.append(f"Add a clear '{name}' heading so the ATS can find that section.")

    # ---- 3. contact (10) ----
    has_email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text) is not None
    has_phone = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text) is not None
    has_link = _has(lowered, "linkedin") or _has(lowered, "github")
    contact_points = (4 if has_email else 0) + (3 if has_phone else 0) + (3 if has_link else 0)
    breakdown.append({"label": "Contact details", "got": contact_points, "max": 10,
                      "note": ", ".join(n for n, ok in (("email", has_email), ("phone", has_phone),
                                                         ("LinkedIn/GitHub", has_link)) if ok) or "none found"})
    if not has_email:
        tips.append("Put your email address at the top of the resume.")
    if not has_phone:
        tips.append("Add a phone number in the header.")
    if not has_link:
        tips.append("Add your LinkedIn or GitHub link.")

    # ---- 4. content quality (20) ----
    verbs_used = [v for v in ACTION_VERBS if _has(lowered, v)]
    numbers = re.findall(r"\d+\s?(?:%|\+|k\b|x\b)|\b\d{2,}\b", text)
    bullets = len(re.findall(r"^\s*[-•*▪●◦]", text, flags=re.M))
    verb_pts = min(8, len(verbs_used) * 2)
    num_pts = min(6, len(numbers) * 2)
    bullet_pts = 6 if bullets >= 5 else (3 if bullets >= 2 else 0)
    breakdown.append({"label": "Content quality", "got": verb_pts + num_pts + bullet_pts, "max": 20,
                      "note": f"{len(verbs_used)} action verbs, {len(numbers)} numbers, {bullets} bullet points"})
    if len(verbs_used) < 4:
        tips.append("Start bullet points with action verbs such as built, developed, improved or deployed.")
    if len(numbers) < 3:
        tips.append("Add numbers that show results, like 'reduced load time by 30%' or 'served 500 users'.")
    if bullets < 5:
        tips.append("Use bullet points (one achievement per line) instead of long paragraphs.")

    # ---- 5. length & format (15) ----
    if 250 <= word_count <= 800:
        len_pts, len_note = 15, f"{word_count} words (ideal range)"
    elif 150 <= word_count < 250 or 800 < word_count <= 1100:
        len_pts, len_note = 9, f"{word_count} words (a little off the ideal 250-800)"
    elif word_count >= 60:
        len_pts, len_note = 4, f"{word_count} words (far from the ideal 250-800)"
    else:
        len_pts, len_note = 0, f"only {word_count} words were readable"
    breakdown.append({"label": "Length & format", "got": len_pts, "max": 15, "note": len_note})
    if word_count < 250:
        tips.append("Your resume looks short. Add project details, tools used and what you achieved.")
    elif word_count > 800:
        tips.append("Your resume is long. Keep it to one or two pages with the strongest points.")

    score = sum(item["got"] for item in breakdown)
    if score >= 80:
        label = "Excellent - ATS friendly"
    elif score >= 60:
        label = "Good - a few fixes will help"
    elif score >= 40:
        label = "Average - needs improvement"
    else:
        label = "Low - needs a big update"
    return {"score": score, "label": label, "breakdown": breakdown, "matched": matched,
            "missing": missing, "sections": found_sections, "tips": tips[:8],
            "word_count": word_count, "keyword_source": source}
