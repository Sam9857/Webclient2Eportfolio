# Skill Check - Resume Quiz (Flask + PostgreSQL)

A simple Flask web app with a sidebar dashboard, plain HTML and one CSS file per page:

| Menu | What it does |
|------|--------------|
| **Dashboard** | Three main cards (quiz, ATS, notes) and your recent quizzes |
| **Resume quiz** | Upload a resume (optional), pick track, topics and 5-60 questions. Past attempts are under "See all history" on the dashboard |
| **ATS score** | Upload a resume (.pdf/.txt) and get a 100-point ATS score with tips |
| **My notes** | Create, edit, pin, search and delete notes |

Plus Register, Login, Logout and Forgot / Reset password (stored in PostgreSQL), .

## Folder structure

```
resume-quiz-flask/
├── app.py                 # all routes
├── database.py            # PostgreSQL connection (connect_db)
├── models.py              # User, QuizAttempt, AtsReport, Note tables
├── sample_data.py         # 60 questions
├── services/              # resume_reader.py (PDF/TXT) and ats.py (scoring)
├── templates/
│   ├── base.html          # bare page: links common.css
│   ├── layout.html        # sidebar + top bar for logged-in pages
│   ├── auth_base.html     # two-column frame for login-style pages
│   ├── _note_fields.html  # form fields shared by new/edit note
│   └── login, register, forgot_password, reset_password, dashboard,
│       quiz_new, quiz, results, ats, ats_report, notes, note_edit, history .html
├── static/css/
│   ├── common.css         # colours, buttons, forms, boxes (every page)
│   ├── layout.css         # sidebar + top bar (logged-in pages)
│   ├── auth.css           # login, register, forgot, reset password
│   └── one file per page: dashboard, quiz-setup, quiz, results,
│       history, ats, ats-report, notes, note-edit .css
├── static/js/main.js      # delete confirm, quiz slider number, quiz progress bar
└── uploads/               # uploaded resumes are saved here
```

Each page links `common.css`, then `layout.css` (logged-in pages), then its own css file.
To change the main colour, edit the `:root` block at the top of `common.css`.

## Run it

1. Start PostgreSQL on **localhost:2005** (details are in `database.py`).
2. `pip install -r requirements.txt`
3. `python app.py` and open http://127.0.0.1:5000
4. Register, then login.

New tables (`quiz_attempts`, `ats_reports`, `notes`) are created automatically on start.
Your existing `app_users` table is not changed, so current accounts keep working.

## Notes

- The reset link is shown on the page ("Demo mode"). A real site would email it.
- ATS scoring is rule-based (keywords, sections, contact info, action verbs, numbers, length). It is a guide, not the exact score of any real ATS.
- Scanned (image-only) PDFs have no text to read. Use a text PDF or .txt.
- Move the database password and `app.secret_key` to environment variables before real use.
