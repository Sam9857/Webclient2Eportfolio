"""Database tables."""
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


class User(db.Model):
    # "app_users" (not "users") so it never clashes with a table you may already have
    __tablename__ = "app_users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # used by "Forgot password"
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class QuizAttempt(db.Model):
    """One finished quiz (shown in History and on the Dashboard)."""
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_users.id"), nullable=False, index=True)
    role = db.Column(db.String(120), nullable=False)
    track = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    pct = db.Column(db.Integer, nullable=False)
    question_ids = db.Column(db.JSON, nullable=False)   # [3, 17, 8, ...]
    answers = db.Column(db.JSON, nullable=False)        # {"3": 1, "17": null, ...}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AtsReport(db.Model):
    """One ATS score report for an uploaded resume."""
    __tablename__ = "ats_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_users.id"), nullable=False, index=True)
    resume_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    details = db.Column(db.JSON, nullable=False)        # full breakdown from services/ats.py
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Note(db.Model):
    """A saved study note."""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_users.id"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False, default="")
    tag = db.Column(db.String(40), nullable=True)
    color = db.Column(db.String(12), nullable=False, default="indigo")
    pinned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
