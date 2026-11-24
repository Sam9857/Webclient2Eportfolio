<<<<<<< HEAD
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
=======
# HTML Assignments - Solutions

Solutions to **HTML Assignment 3 (Forms)** and **HTML Assignment 4 (HTML5)**.
Every question has its own standalone `.html` file - just open it in a browser.

## Project Structure

```
html-assignments/
├── README.md
├── assignment-3-forms/
│   ├── basic/          (20 files)
│   ├── intermediate/   (20 files)
│   └── advanced/       (10 files)
└── assignment-4-html5/
    ├── basic/          (19 files)
    ├── intermediate/   (20 files)
    └── advanced/       (10 files)
```

## How to Run

1. Clone or download this repository.
2. Open any `.html` file in your browser (double-click it), or use the *Live Server* extension in VS Code.

No build tools, frameworks or internet connection are needed.

---

## Assignment 3 - Forms

### Basic Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Create a simple HTML form with a single text input field for entering a username. | [`01-username-input.html`](assignment-3-forms/basic/01-username-input.html) |
| 2 | Build a form with a password input field that hides typed characters. | [`02-password-input.html`](assignment-3-forms/basic/02-password-input.html) |
| 3 | Make a form that includes two text fields: First Name and Last Name. | [`03-first-last-name.html`](assignment-3-forms/basic/03-first-last-name.html) |
| 4 | Add a submit button in a form that sends data when clicked. | [`04-submit-button.html`](assignment-3-forms/basic/04-submit-button.html) |
| 5 | Create a form with a reset button that clears the inputs. | [`05-reset-button.html`](assignment-3-forms/basic/05-reset-button.html) |
| 6 | Create a form with radio buttons for selecting gender (Male/Female). | [`06-gender-radio.html`](assignment-3-forms/basic/06-gender-radio.html) |
| 7 | Make a form with checkboxes for selecting hobbies (e.g., Reading, Sports, Coding). | [`07-hobbies-checkbox.html`](assignment-3-forms/basic/07-hobbies-checkbox.html) |
| 8 | Add a form with a file upload input to let users upload a profile picture. | [`08-file-upload.html`](assignment-3-forms/basic/08-file-upload.html) |
| 9 | Use the <label> tag to correctly label a text input field. | [`09-label-tag.html`](assignment-3-forms/basic/09-label-tag.html) |
| 10 | Create a dropdown menu using <select> with options for choosing a country. | [`10-country-dropdown.html`](assignment-3-forms/basic/10-country-dropdown.html) |
| 11 | Build a form that includes a textarea for user comments. | [`11-textarea-comments.html`](assignment-3-forms/basic/11-textarea-comments.html) |
| 12 | Create a form with a button element labelled “Click Me”. | [`12-click-me-button.html`](assignment-3-forms/basic/12-click-me-button.html) |
| 13 | Add a required attribute in a text input field for entering a name. | [`13-required-name.html`](assignment-3-forms/basic/13-required-name.html) |
| 14 | Build a form with type=”email” input and test validation. | [`14-email-validation.html`](assignment-3-forms/basic/14-email-validation.html) |
| 15 | Create a form with a number input for entering age. | [`15-age-number.html`](assignment-3-forms/basic/15-age-number.html) |
| 16 | Add a date picker input to select a birthdate. | [`16-birthdate-picker.html`](assignment-3-forms/basic/16-birthdate-picker.html) |
| 17 | Create a form with a time input for selecting appointment time. | [`17-appointment-time.html`](assignment-3-forms/basic/17-appointment-time.html) |
| 18 | Add a colour input where users can pick a favourite color. | [`18-favourite-color.html`](assignment-3-forms/basic/18-favourite-color.html) |
| 19 | Create a range input for selecting volume level (1-100). | [`19-volume-range.html`](assignment-3-forms/basic/19-volume-range.html) |
| 20 | Use <fieldset> and <legend> to group personal details inputs (name, email). | [`20-fieldset-legend.html`](assignment-3-forms/basic/20-fieldset-legend.html) |

### Intermediate Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Create a login form with username and password fields, and a submit button. | [`01-login-form.html`](assignment-3-forms/intermediate/01-login-form.html) |
| 2 | Create a contact form containing Name, Email, Phone, and Message fields. | [`02-contact-form.html`](assignment-3-forms/intermediate/02-contact-form.html) |
| 3 | Add radio buttons for “Payment Method” (Credit Card, UPI, Cash on Delivery). | [`03-payment-method.html`](assignment-3-forms/intermediate/03-payment-method.html) |
| 4 | Use checkboxes for selecting multiple languages (English, Hindi, French, Spanish). | [`04-languages-checkbox.html`](assignment-3-forms/intermediate/04-languages-checkbox.html) |
| 5 | Create a form where the age input is restricted between 18-60 using min and max attributes. | [`05-age-min-max.html`](assignment-3-forms/intermediate/05-age-min-max.html) |
| 6 | Build a form that has pattern validation for a 10-digit phone number. | [`06-phone-pattern.html`](assignment-3-forms/intermediate/06-phone-pattern.html) |
| 7 | Create a file upload form where only PDF files are allowed using the accept attribute. | [`07-pdf-upload.html`](assignment-3-forms/intermediate/07-pdf-upload.html) |
| 8 | Add a dropdown to select a user’s profession (Student, Teacher, Developer, Designer). | [`08-profession-dropdown.html`](assignment-3-forms/intermediate/08-profession-dropdown.html) |
| 9 | Create a form that disables the submit button until terms & conditions are checked. | [`09-terms-disable-submit.html`](assignment-3-forms/intermediate/09-terms-disable-submit.html) |
| 10 | Build a form using <fieldset> and <legend> for grouping address details. | [`10-address-fieldset.html`](assignment-3-forms/intermediate/10-address-fieldset.html) |
| 11 | Create a form where email input must follow correct format (e.g., abc@mail.com). | [`11-email-format.html`](assignment-3-forms/intermediate/11-email-format.html) |
| 12 | Add a placeholder attribute in inputs for guiding user entries. | [`12-placeholder-attribute.html`](assignment-3-forms/intermediate/12-placeholder-attribute.html) |
| 13 | Create a form using password input with a “Confirm Password” field. | [`13-confirm-password.html`](assignment-3-forms/intermediate/13-confirm-password.html) |
| 14 | Make a form with a reset button and test clearing inputs. | [`14-reset-test.html`](assignment-3-forms/intermediate/14-reset-test.html) |
| 15 | Create a newsletter signup form with Name, Email, and a Subscribe button. | [`15-newsletter-signup.html`](assignment-3-forms/intermediate/15-newsletter-signup.html) |
| 16 | Add a disabled input field in a form (show readonly behavior). | [`16-disabled-readonly.html`](assignment-3-forms/intermediate/16-disabled-readonly.html) |
| 17 | Create a form with hidden input fields (like a user ID). | [`17-hidden-input.html`](assignment-3-forms/intermediate/17-hidden-input.html) |
| 18 | Add a form where the range input shows values from 1 to 10 for rating experience. | [`18-rating-range-1-10.html`](assignment-3-forms/intermediate/18-rating-range-1-10.html) |
| 19 | Design a colour picker form allowing users to set background colour. | [`19-background-color-picker.html`](assignment-3-forms/intermediate/19-background-color-picker.html) |
| 20 | Build a form using tel input type for phone number formatting. | [`20-tel-input.html`](assignment-3-forms/intermediate/20-tel-input.html) |

### Advanced Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Create a registration form with full validation (Name, Email, Password, Confirm Password, Gender, Country). | [`01-registration-form.html`](assignment-3-forms/advanced/01-registration-form.html) |
| 2 | Make a form where passwords must meet a pattern (8+ characters, at least 1 capital, 1 number). | [`02-password-pattern.html`](assignment-3-forms/advanced/02-password-pattern.html) |
| 3 | Create a multi-step form: Step 1 (Personal Info), Step 2 (Contact Info), Step 3 (Submit). | [`03-multi-step-form.html`](assignment-3-forms/advanced/03-multi-step-form.html) |
| 4 | Build a survey form with a mix of text, radio, checkbox, dropdown, and textarea inputs. | [`04-survey-form.html`](assignment-3-forms/advanced/04-survey-form.html) |
| 5 | Create a job application form with File Upload restricted to only PDFs or DOCs. | [`05-job-application.html`](assignment-3-forms/advanced/05-job-application.html) |
| 6 | Create a form that disables submit if required fields are empty. | [`06-disable-submit-until-valid.html`](assignment-3-forms/advanced/06-disable-submit-until-valid.html) |
| 7 | Add ARIA labels and roles for accessibility in a form with multiple input types. | [`07-aria-accessible-form.html`](assignment-3-forms/advanced/07-aria-accessible-form.html) |
| 8 | Create a form where the date input must be today or later (for booking purposes). | [`08-booking-date-today-or-later.html`](assignment-3-forms/advanced/08-booking-date-today-or-later.html) |
| 9 | Build a profile settings form with Name, Profile Picture Upload, Colour Theme Picker, and Save button. | [`09-profile-settings.html`](assignment-3-forms/advanced/09-profile-settings.html) |
| 10 | Create a feedback form that includes star rating (radio buttons), comment box, and submit. | [`10-feedback-star-rating.html`](assignment-3-forms/advanced/10-feedback-star-rating.html) |


---

## Assignment 4 - HTML5

### Basic Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Create a simple webpage with a <header> and <footer>. | [`01-header-footer.html`](assignment-4-html5/basic/01-header-footer.html) |
| 2 | Write HTML to display a website title inside the <header>. | [`02-website-title-header.html`](assignment-4-html5/basic/02-website-title-header.html) |
| 3 | Add a <nav> element with 3 links: Home, About, Contact. | [`03-nav-three-links.html`](assignment-4-html5/basic/03-nav-three-links.html) |
| 4 | Display a paragraph inside the <main> element on a webpage. | [`04-main-paragraph.html`](assignment-4-html5/basic/04-main-paragraph.html) |
| 5 | Create a page that uses <section> for displaying two different topics. | [`05-two-sections.html`](assignment-4-html5/basic/05-two-sections.html) |
| 6 | Use an <article> tag to display a blog post with a heading and a paragraph. | [`06-article-blog-post.html`](assignment-4-html5/basic/06-article-blog-post.html) |
| 7 | Insert an image inside a <figure> element with a <figcaption>. | [`07-figure-figcaption.html`](assignment-4-html5/basic/07-figure-figcaption.html) |
| 8 | Use <time> tag to represent today’s date in an event description. | [`08-time-today.html`](assignment-4-html5/basic/08-time-today.html) |
| 9 | Write HTML that displays your contact info using <address>. | [`09-address-contact.html`](assignment-4-html5/basic/09-address-contact.html) |
| 10 | Create a webpage with <header>, <main>, and <footer> layout. | [`10-header-main-footer.html`](assignment-4-html5/basic/10-header-main-footer.html) |
| 11 | Add a <nav> with links that display horizontally. | [`11-nav-horizontal.html`](assignment-4-html5/basic/11-nav-horizontal.html) |
| 12 | Display the publication date of an article using <time>. | [`12-article-publication-date.html`](assignment-4-html5/basic/12-article-publication-date.html) |
| 13 | Create a simple blog page with one <article> inside <main>. | [`13-simple-blog-page.html`](assignment-4-html5/basic/13-simple-blog-page.html) |
| 14 | Write HTML to show two images with their captions using <figure> and <figcaption>. | [`14-two-figures.html`](assignment-4-html5/basic/14-two-figures.html) |
| 15 | Display the website developer’s email address using <address>. | [`15-developer-email-address.html`](assignment-4-html5/basic/15-developer-email-address.html) |
| 16 | Draw a rectangle using inline <svg>. | [`16-svg-rectangle.html`](assignment-4-html5/basic/16-svg-rectangle.html) |
| 17 | Draw a circle using <svg>. | [`17-svg-circle.html`](assignment-4-html5/basic/17-svg-circle.html) |
| 18 | Draw a line using SVG between two points. | [`18-svg-line.html`](assignment-4-html5/basic/18-svg-line.html) |
| 19 | Create a simple <canvas> element with a border. | [`19-canvas-border.html`](assignment-4-html5/basic/19-canvas-border.html) |

### Intermediate Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Create a webpage layout with <header>, <nav>, <main>, <aside>, and <footer>. | [`01-five-part-layout.html`](assignment-4-html5/intermediate/01-five-part-layout.html) |
| 2 | Write HTML with multiple <section> elements under <main> to display different categories. | [`02-multiple-sections-categories.html`](assignment-4-html5/intermediate/02-multiple-sections-categories.html) |
| 3 | Build a blog post with <article> and show its author info in <address>. | [`03-article-author-address.html`](assignment-4-html5/intermediate/03-article-author-address.html) |
| 4 | Create a page that uses <header> for navigation and <footer> for copyright. | [`04-header-nav-footer-copyright.html`](assignment-4-html5/intermediate/04-header-nav-footer-copyright.html) |
| 5 | Use <article> tags to add two different blog posts inside <main>. | [`05-two-articles-in-main.html`](assignment-4-html5/intermediate/05-two-articles-in-main.html) |
| 6 | Include one <aside> section showing related articles in a blog page. | [`06-aside-related-articles.html`](assignment-4-html5/intermediate/06-aside-related-articles.html) |
| 7 | Display one image with a title using <figure> and <figcaption> inside <section>. | [`07-figure-in-section.html`](assignment-4-html5/intermediate/07-figure-in-section.html) |
| 8 | Use <time> to mark the date and time of an event (like “Published on 20 August 2025, 5:00 PM”). | [`08-time-event-datetime.html`](assignment-4-html5/intermediate/08-time-event-datetime.html) |
| 9 | Design a company’s contact page using <address> with location, phone, and email. | [`09-company-contact-address.html`](assignment-4-html5/intermediate/09-company-contact-address.html) |
| 10 | Write HTML to structure a magazine-like layout using <section> and <article>. | [`10-magazine-layout.html`](assignment-4-html5/intermediate/10-magazine-layout.html) |
| 11 | Draw a blue rectangle inside an SVG. | [`11-svg-blue-rectangle.html`](assignment-4-html5/intermediate/11-svg-blue-rectangle.html) |
| 12 | Create an SVG with both a circle and rectangle. | [`12-svg-circle-and-rectangle.html`](assignment-4-html5/intermediate/12-svg-circle-and-rectangle.html) |
| 13 | Draw a triangle shape using <polygon> in SVG. | [`13-svg-triangle-polygon.html`](assignment-4-html5/intermediate/13-svg-triangle-polygon.html) |
| 14 | Create an inline SVG with a line connecting two circles. | [`14-svg-line-connecting-circles.html`](assignment-4-html5/intermediate/14-svg-line-connecting-circles.html) |
| 15 | Make a canvas with a red filled rectangle using JavaScript. | [`15-canvas-red-rectangle.html`](assignment-4-html5/intermediate/15-canvas-red-rectangle.html) |
| 16 | Draw a diagonal line on a canvas from top-left to bottom-right. | [`16-canvas-diagonal-line.html`](assignment-4-html5/intermediate/16-canvas-diagonal-line.html) |
| 17 | Use <canvas> to draw a filled blue circle. | [`17-canvas-blue-circle.html`](assignment-4-html5/intermediate/17-canvas-blue-circle.html) |
| 18 | Display multiple shapes (circle, rectangle, line) inside a single <canvas>. | [`18-canvas-multiple-shapes.html`](assignment-4-html5/intermediate/18-canvas-multiple-shapes.html) |
| 19 | Add an SVG ellipse and style it using fill=”green”. | [`19-svg-green-ellipse.html`](assignment-4-html5/intermediate/19-svg-green-ellipse.html) |
| 20 | Write HTML with a <header>, <main>, <aside>, and <footer> plus an inline SVG below the main content. | [`20-layout-with-svg.html`](assignment-4-html5/intermediate/20-layout-with-svg.html) |

### Advanced Questions

| # | Question | Solution |
|---|----------|----------|
| 1 | Build a complete semantic webpage layout using <header>, <nav>, <main>, <article>, <aside>, <footer> with actual demo content. | [`01-complete-semantic-layout.html`](assignment-4-html5/advanced/01-complete-semantic-layout.html) |
| 2 | Create a blog webpage with 3 <article> posts, each with <time> and <address> info for the author. | [`02-blog-three-articles.html`](assignment-4-html5/advanced/02-blog-three-articles.html) |
| 3 | Combine <figure> with image thumbnails, each having captions (like a mini photo gallery). | [`03-photo-gallery-figures.html`](assignment-4-html5/advanced/03-photo-gallery-figures.html) |
| 4 | Design a newspaper layout using <section>, <article>, and <aside> with proper structure. | [`04-newspaper-layout.html`](assignment-4-html5/advanced/04-newspaper-layout.html) |
| 5 | Draw a sunset scene in SVG (sun = circle, ground = rectangle, rays = lines). | [`05-svg-sunset-scene.html`](assignment-4-html5/advanced/05-svg-sunset-scene.html) |
| 6 | Write JavaScript to draw a house shape on <canvas> (rectangle for house, triangle for roof, square for window). | [`06-canvas-house.html`](assignment-4-html5/advanced/06-canvas-house.html) |
| 7 | Use <canvas> to fill two rectangles with linear gradient colors. | [`07-canvas-linear-gradients.html`](assignment-4-html5/advanced/07-canvas-linear-gradients.html) |
| 8 | Create a small bouncing ball animation using <canvas> and JavaScript. | [`08-canvas-bouncing-ball.html`](assignment-4-html5/advanced/08-canvas-bouncing-ball.html) |
| 9 | Build a webpage that has a semantic structure and an inline SVG chart (e.g., bar chart using <rect>). | [`09-semantic-page-svg-bar-chart.html`](assignment-4-html5/advanced/09-semantic-page-svg-bar-chart.html) |
| 10 | Create a dashboard page with <header>, <nav>, <main>, <aside>, <footer>, plus an animated <canvas> graph. | [`10-dashboard-animated-canvas.html`](assignment-4-html5/advanced/10-dashboard-animated-canvas.html) |


---

## Topics Covered

- **Assignment 3:** text/password/email/number/date/time/color/range/tel/file/hidden inputs, radio buttons, checkboxes, `<select>`, `<textarea>`, `<label>`, `<fieldset>`/`<legend>`, validation (`required`, `pattern`, `min`/`max`, `accept`), disabled/readonly, ARIA, multi-step forms.
- **Assignment 4:** semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<figure>`, `<time>`, `<address>`), inline SVG shapes and charts, and Canvas drawing and animation.
>>>>>>> c005dd3d314ef0f42b36c568bb4c992f7152f756
