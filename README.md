# Anitha Portfolio (Django) with an AI voice guide

A single-page, dark "glass" portfolio built on your existing Django project
(same `main` app, `Project` model, admin, contact form and URL names).
The **AI voice guide** reads the portfolio aloud: it highlights each card as it is
spoken, shows live captions, and lets visitors pick a topic or play a full tour.

## Run it locally

```bash
python -m venv venv
venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_projects          # your 24 live projects (images are in /media)
python manage.py createsuperuser        # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000 and press **Hear the intro** (or the **Listen** button, bottom-right).

## The AI voice guide

* Uses the browser's built-in text-to-speech (Web Speech API): free, no API key,
  nothing is sent to any server, and **it never plays until a visitor presses a button**.
* Topics: Intro, About, Skills, Projects, Journey, Contact, and a Full tour.
  Every section title also has its own **Listen** button.
* Controls: play/pause, previous/next, stop, speed, and voice (English voices;
  Indian English is preferred when the device has it). Choices are remembered.
* Works in Chrome, Edge and Safari. Voice quality depends on the visitor's device
  (Edge's "Natural" voices and Chrome's Google voices sound best).
* Firefox or browsers without speech support show a short notice instead.

### Changing what it says
* Skills, experience, education, contacts and the intro text live in **`main/content.py`**.
  Edit there and both the page and the audio update.
* In templates, any element with `data-say="..."` is one spoken chunk
  (`data-say=""` reads the element's visible text). Sections are grouped by `data-topic`.
* Projects from the admin are read out by title (the first six, then "and more"). If you add a **description** to a project
  in `/admin/`, it is shown on the card and read aloud too.

## Project layout

```
manage.py
requirements.txt
.env.example            copy to .env (secrets go here, never in settings.py)
portfolio/settings.py   reads secrets from environment / .env
main/content.py         all portfolio text + narration
main/views.py           home, contact form (old /about/ and /projects/ redirect to sections)
main/models.py          Project (migration 0003 makes description optional)
main/templates/main/    base.html, index.html, partials/ai_dock.html, email/
static/main/css|js|images|files
media/projects/         project screenshots
main/management/commands/seed_projects.py   the project list (title, image, live link)
```

## Contact form and email
Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` (a Gmail App Password) in `.env`.
Without a password, messages are printed in the terminal, so the form still works while developing.
Hidden honeypot field blocks simple spam bots.

## Deploying (e.g. Render)
1. Set env vars: `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
   `DJANGO_CSRF_TRUSTED_ORIGINS`, `SITE_URL`, `EMAIL_HOST_PASSWORD`.
2. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_projects`
3. Start: `gunicorn portfolio.wsgi`

Static files are served by WhiteNoise. Project images in `media/` are served by Django.
Files uploaded later through the admin are lost on hosts with temporary disks,
so keep new project images in the repository or use external storage.

## Tests
`python manage.py test`

## Things to double-check
* **Rotate your Gmail app password.** The old `settings.py` contained it in plain text,
  so treat it as exposed and create a new one in your Google account.
* `main/content.py` says **Anna University, Virudhunagar** (old site); your newest CV says
  **Tirunelveli**. Change `BTECH_PLACE` if the CV is right.
* The CV button uses `static/main/files/Anitha_CV.pdf` (the old PDF). To use the newer
  `Anitha_CCV.docx`, export it to PDF and replace that file.
* The Facebook link now uses `facebook.com/AnithaSaravanan` (the old home page link had a space in it).

## Adding or changing projects
* Edit the `PROJECTS` list in `main/management/commands/seed_projects.py` and run
  `python manage.py seed_projects` again (safe to repeat; descriptions written in `/admin/` are kept).
* Or add one in `/admin/`. Cover images are 800x500 files in `media/projects/`.
* Car Wash and Vegetable Shop currently point to the Book Store link. Replace them with their own URLs.
