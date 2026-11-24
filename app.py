"""Skill Check - Resume Quiz, ATS Score and Notes (Flask + PostgreSQL + HTML5 + CSS)."""
import os
import random
import re
import secrets
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from sqlalchemy import func
from werkzeug.utils import secure_filename

from database import db, connect_db
from models import AtsReport, Note, QuizAttempt, User
from sample_data import CATEGORIES, QUESTIONS, QUESTION_BY_ID
from services import ats as ats_engine
from services import resume_reader

app = Flask(__name__)
app.secret_key = "change-me-in-real-projects"           # needed for session + flash
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024       # 5 MB upload limit
ALLOWED_EXTENSIONS = {"pdf", "txt"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NOTE_COLORS = ["indigo", "sky", "teal", "emerald", "rose", "violet"]
CATEGORY_COLOR = {"Python": "sky", "Flask": "teal", "HTML & CSS": "rose",
                  "SQL & Databases": "violet", "Git & Web": "emerald", "DSA & CS": "indigo"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ---------- connect to PostgreSQL and create tables ----------
connect_db(app)
with app.app_context():
    try:
        db.create_all()
    except Exception as error:
        raise SystemExit(
            "\nCould not connect to PostgreSQL.\n"
            "Check that PostgreSQL is running on localhost:2005 and the details in database.py are right.\n"
            f"Details: {error}\n"
        )


# ---------- helpers ----------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def uid():
    return session["user_id"]


def password_problem(password, confirm):
    """Return an error message, or None if the password is fine."""
    if len(password) < 6:
        return "Password must be at least 6 characters."
    if password != confirm:
        return "Passwords do not match."
    return None


def verdict_for(pct):
    if pct >= 85:
        return "Strong performance - interview ready!"
    if pct >= 65:
        return "Solid foundation, some gaps to close."
    if pct >= 40:
        return "Needs focused review before interviewing."
    return "Significant gaps - revisit the fundamentals."


def pick_questions(track, count, categories, boost_categories):
    """Choose question ids: right level first, then topics found in the resume."""
    pool = [q for q in QUESTIONS if not categories or q["category"] in categories]
    wanted_level = "basic" if track == "internship" else "advanced"
    random.shuffle(pool)
    pool.sort(key=lambda q: (q["level"] != wanted_level, q["category"] not in boost_categories))
    chosen = pool[:count]
    random.shuffle(chosen)
    return [q["id"] for q in chosen]


def save_upload(file):
    """Save an uploaded resume and return (saved_name, full_path)."""
    name = f"{uid()}_{secure_filename(file.filename)}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], name)
    file.save(path)
    return name, path


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.template_filter("fmt_date")
def fmt_date(value):
    return value.strftime("%d %b %Y, %H:%M") if value else ""


@app.template_filter("short_date")
def short_date(value):
    return value.strftime("%d %b") if value else ""


@app.context_processor
def layout_data():
    """Values the sidebar and top bar need on every logged-in page."""
    if not session.get("user_id"):
        return {}
    user_id = session["user_id"]
    best_ats = db.session.query(func.max(AtsReport.score)).filter_by(user_id=user_id).scalar()
    user = db.session.get(User, user_id)
    return {"best_ats": best_ats, "user_code": f"SC{user_id:03d}",
            "user_email": user.email if user else "",
            "notes_count": Note.query.filter_by(user_id=user_id).count()}


# ---------- authentication ----------
@app.route("/")
def home():
    return redirect(url_for("dashboard" if session.get("user_id") else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    form = {"name": "", "email": ""}
    if request.method == "POST":
        form["name"] = request.form.get("name", "").strip()
        form["email"] = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not form["name"]:
            flash("Please enter your name.", "error")
        elif not EMAIL_PATTERN.match(form["email"]):
            flash("Please enter a valid email address.", "error")
        elif password_problem(password, confirm):
            flash(password_problem(password, confirm), "error")
        elif User.query.filter_by(email=form["email"]).first():
            flash("An account with this email already exists.", "error")
        else:
            user = User(name=form["name"], email=form["email"])
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("dashboard"))
        flash("Incorrect email or password.", "error")
    return render_template("login.html", email=email)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    reset_link = None
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not EMAIL_PATTERN.match(email):
            flash("Please enter a valid email address.", "error")
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                user.reset_token = secrets.token_urlsafe(32)
                user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
                db.session.commit()
                # A real site would EMAIL this link. For the demo we show it on the page.
                reset_link = url_for("reset_password", token=user.reset_token, _external=True)
            flash("If that email is registered, a password reset link has been created.", "success")
    return render_template("forgot_password.html", email=email, reset_link=reset_link)


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        flash("This reset link is invalid or has expired. Please request a new one.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        problem = password_problem(password, confirm)
        if problem:
            flash(problem, "error")
        else:
            user.set_password(password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            flash("Password updated! Please login with your new password.", "success")
            return redirect(url_for("login"))
    return render_template("reset_password.html", token=token)


# ---------- dashboard ----------
@app.route("/dashboard")
@login_required
def dashboard():
    attempts = QuizAttempt.query.filter_by(user_id=uid())
    stats = {
        "quizzes": attempts.count(),
        "best_quiz": db.session.query(func.max(QuizAttempt.pct)).filter_by(user_id=uid()).scalar(),
        "notes": Note.query.filter_by(user_id=uid()).count(),
        "pinned": Note.query.filter_by(user_id=uid(), pinned=True).count(),
    }
    recent = attempts.order_by(QuizAttempt.created_at.desc()).limit(5).all()
    latest_ats = (AtsReport.query.filter_by(user_id=uid())
                  .order_by(AtsReport.created_at.desc()).first())
    return render_template("dashboard.html", stats=stats, recent=recent,
                           latest_ats=latest_ats, total_questions=len(QUESTIONS))


# ---------- quiz ----------
@app.route("/quiz/new", methods=["GET", "POST"])
@login_required
def quiz_new():
    if request.method == "POST":
        file = request.files.get("resume")
        track = request.form.get("track", "internship")
        track = track if track in ("internship", "experienced") else "internship"
        role = request.form.get("role", "").strip()
        picked = [c for c in request.form.getlist("category") if c in CATEGORIES]
        try:
            num = int(request.form.get("num_questions", 10))
        except ValueError:
            num = 10

        has_file = file is not None and file.filename != ""
        if has_file and not allowed(file.filename):
            flash("Only .pdf or .txt files are allowed.", "error")
        elif not role:
            flash("Please enter your target role.", "error")
        else:
            skills = []
            if has_file:
                _, path = save_upload(file)
                try:
                    skills = resume_reader.find_skills(resume_reader.extract_text(path))
                except Exception:
                    flash("We could not read that resume, so questions were not matched to it.", "error")
            boost = resume_reader.categories_for(skills)
            pool_size = len([q for q in QUESTIONS if not picked or q["category"] in picked])
            count = max(5, min(num, pool_size))
            session["setup"] = {"role": role, "track": track,
                                "question_ids": pick_questions(track, count, picked, boost),
                                "skills": skills[:12]}
            return redirect(url_for("quiz"))
    preset = {"n": request.args.get("n", type=int) or 10,
              "cat": request.args.get("cat", "")}
    return render_template("quiz_new.html", categories=CATEGORIES,
                           max_questions=len(QUESTIONS), preset=preset)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    setup = session.get("setup")
    if not setup:
        return redirect(url_for("quiz_new"))
    questions = [QUESTION_BY_ID[i] for i in setup["question_ids"]]
    if request.method == "POST":
        answers = {str(q["id"]): request.form.get(f"q{q['id']}", type=int) for q in questions}
        score = sum(1 for q in questions if answers[str(q["id"])] == q["correct_index"])
        attempt = QuizAttempt(user_id=uid(), role=setup["role"], track=setup["track"],
                              score=score, total=len(questions),
                              pct=round(score / len(questions) * 100),
                              question_ids=setup["question_ids"], answers=answers)
        db.session.add(attempt)
        db.session.commit()
        session.pop("setup", None)
        return redirect(url_for("results", attempt_id=attempt.id))
    return render_template("quiz.html", questions=questions, setup=setup)


@app.route("/results/<int:attempt_id>")
@login_required
def results(attempt_id):
    attempt = QuizAttempt.query.filter_by(id=attempt_id, user_id=uid()).first_or_404()
    graded, by_cat = [], {}
    for qid in attempt.question_ids:
        q = QUESTION_BY_ID[qid]
        selected = attempt.answers.get(str(qid))
        ok = selected == q["correct_index"]
        graded.append({**q, "selected_index": selected, "is_correct": ok})
        bucket = by_cat.setdefault(q["category"], {"right": 0, "total": 0})
        bucket["total"] += 1
        bucket["right"] += 1 if ok else 0
    only_missed = request.args.get("filter") == "missed"
    shown = [g for g in graded if not g["is_correct"]] if only_missed else graded
    categories = [{"name": n, "right": v["right"], "total": v["total"],
                   "pct": round(v["right"] / v["total"] * 100), "color": CATEGORY_COLOR[n]}
                  for n, v in by_cat.items()]
    return render_template("results.html", attempt=attempt, shown=shown,
                           categories=categories, verdict=verdict_for(attempt.pct),
                           only_missed=only_missed)


@app.route("/history")
@login_required
def history():
    attempts = (QuizAttempt.query.filter_by(user_id=uid())
                .order_by(QuizAttempt.created_at.desc()).all())
    reports = (AtsReport.query.filter_by(user_id=uid())
               .order_by(AtsReport.created_at.desc()).all())
    best = max((a.pct for a in attempts), default=None)
    average = round(sum(a.pct for a in attempts) / len(attempts)) if attempts else None
    return render_template("history.html", attempts=attempts, reports=reports,
                           best=best, average=average)


# ---------- ATS score ----------
@app.route("/ats", methods=["GET", "POST"])
@login_required
def ats():
    if request.method == "POST":
        file = request.files.get("resume")
        role = request.form.get("role", "").strip()
        job_description = request.form.get("job_description", "")
        if not file or file.filename == "":
            flash("Please choose your resume file.", "error")
        elif not allowed(file.filename):
            flash("Only .pdf or .txt files are allowed.", "error")
        else:
            name, path = save_upload(file)
            try:
                text = resume_reader.extract_text(path)
            except Exception:
                text = ""
            if len(text) < 30:
                flash("We could not read any text in this file. Scanned PDFs need to be saved as a text-based PDF or .txt.", "error")
            else:
                result = ats_engine.analyze(text, role, job_description)
                report = AtsReport(user_id=uid(), resume_name=name.split("_", 1)[-1],
                                   role=role or "General", score=result["score"], details=result)
                db.session.add(report)
                db.session.commit()
                return redirect(url_for("ats_report", report_id=report.id))
    reports = (AtsReport.query.filter_by(user_id=uid())
               .order_by(AtsReport.created_at.desc()).limit(5).all())
    return render_template("ats.html", reports=reports)


@app.route("/ats/<int:report_id>")
@login_required
def ats_report(report_id):
    report = AtsReport.query.filter_by(id=report_id, user_id=uid()).first_or_404()
    return render_template("ats_report.html", report=report, d=report.details)


@app.route("/ats/<int:report_id>/delete", methods=["POST"])
@login_required
def ats_delete(report_id):
    report = AtsReport.query.filter_by(id=report_id, user_id=uid()).first_or_404()
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "success")
    return redirect(url_for("ats"))


# ---------- notes ----------
def clean_note_form():
    title = request.form.get("title", "").strip()[:150]
    content = request.form.get("content", "").strip()
    tag = request.form.get("tag", "").strip()[:40] or None
    color = request.form.get("color", "indigo")
    return title, content, tag, color if color in NOTE_COLORS else "indigo"


@app.route("/notes")
@login_required
def notes():
    q = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    pinned_only = request.args.get("pinned") == "1"
    query = Note.query.filter_by(user_id=uid())
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Note.title.ilike(like), Note.content.ilike(like)))
    if tag:
        query = query.filter_by(tag=tag)
    if pinned_only:
        query = query.filter_by(pinned=True)
    items = query.order_by(Note.pinned.desc(), Note.updated_at.desc()).all()
    tags = [t for (t,) in db.session.query(Note.tag).filter(
        Note.user_id == uid(), Note.tag.isnot(None)).distinct().order_by(Note.tag).all()]
    return render_template("notes.html", notes=items, tags=tags, q=q, tag=tag,
                           pinned_only=pinned_only, colors=NOTE_COLORS)


@app.route("/notes/new", methods=["POST"])
@login_required
def note_create():
    title, content, tag, color = clean_note_form()
    if not title:
        flash("Please give your note a title.", "error")
    else:
        db.session.add(Note(user_id=uid(), title=title, content=content, tag=tag, color=color))
        db.session.commit()
        flash("Note saved.", "success")
    return redirect(url_for("notes"))


@app.route("/notes/<int:note_id>", methods=["GET", "POST"])
@login_required
def note_edit(note_id):
    note = Note.query.filter_by(id=note_id, user_id=uid()).first_or_404()
    if request.method == "POST":
        title, content, tag, color = clean_note_form()
        if not title:
            flash("Please give your note a title.", "error")
        else:
            note.title, note.content, note.tag, note.color = title, content, tag, color
            db.session.commit()
            flash("Note updated.", "success")
            return redirect(url_for("notes"))
    return render_template("note_edit.html", note=note, colors=NOTE_COLORS)


@app.route("/notes/<int:note_id>/pin", methods=["POST"])
@login_required
def note_pin(note_id):
    note = Note.query.filter_by(id=note_id, user_id=uid()).first_or_404()
    note.pinned = not note.pinned
    db.session.commit()
    return redirect(request.referrer or url_for("notes"))


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def note_delete(note_id):
    note = Note.query.filter_by(id=note_id, user_id=uid()).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "success")
    return redirect(url_for("notes"))


@app.route("/notes/from-question", methods=["POST"])
@login_required
def note_from_question():
    """'Save to notes' button on the results page."""
    qid = request.form.get("question_id", type=int)
    attempt_id = request.form.get("attempt_id", type=int)
    q = QUESTION_BY_ID.get(qid)
    if not q or not attempt_id:
        abort(400)
    content = (f"Question: {q['question']}\n\nCorrect answer: {q['options'][q['correct_index']]}"
               f"\n\nWhy: {q['explanation']}")
    db.session.add(Note(user_id=uid(), title=f"Review: {q['question'][:110]}", content=content,
                        tag=q["category"], color=CATEGORY_COLOR[q["category"]]))
    db.session.commit()
    flash("Saved to your notes.", "success")
    return redirect(url_for("results", attempt_id=attempt_id, filter=request.form.get("filter") or None))


@app.errorhandler(413)
def too_large(_):
    flash("File is too large (max 5 MB).", "error")
    return redirect(request.referrer or url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
