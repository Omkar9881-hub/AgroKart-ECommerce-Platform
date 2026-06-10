# Copilot Instructions for AgroKart Django Project

## Project Overview
- **AgroKart** is a Django-based web application for digital agriculture, connecting farmers with seed suppliers and providing a multilingual, user-friendly platform.
- The main Django app is `core`. All business logic, views, and templates are under this app.
- The project is structured as a standard Django project with custom templates, static files, and user authentication.

## Key Components & Structure
- **manage.py**: Entry point for all management commands (runserver, migrate, createsuperuser, etc).
- **Agrokart/settings.py**: Django settings (apps, middleware, static files, etc).
- **core/**: Main app containing:
  - `models.py`: (Minimal, extend for DB models)
  - `views.py`: All view logic (signup, login, home, about, product, etc)
  - `urls.py`: App-level URL routing
  - `templates/core/`: All HTML templates (e.g., `home.html`)
  - `static/`: Static assets (images, CSS, JS)

## Developer Workflows
- **Run locally:**
  ```sh
  python manage.py runserver
  ```
- **Migrate DB:**
  ```sh
  python manage.py migrate
  ```
- **Create superuser:**
  ```sh
  python manage.py createsuperuser
  ```
- **Install dependencies:**
  ```sh
  pip install -r requirements.txt
  ```

## Project Conventions
- **Templates:** Use Django template language (`{% %}` and `{{ }}`) for dynamic content and static file loading.
- **Static files:** Place images, CSS, JS in `core/static/` and reference with `{% static %}`.
- **Multilingual:** Use `lang-text` class and `data-en`, `data-mr` attributes for English/Marathi switching (see `home.html` for pattern).
- **User Data:** User location is temporarily stored in the `first_name` field (see `signup_view`).
- **Views:** All user-facing logic is in `core/views.py`. Each page has a corresponding view and template.
- **URLs:** All routes are defined in `core/urls.py` and included in the main project URLs.

## Patterns & Integrations
- **No custom models yet:** Extend `core/models.py` for new DB tables.
- **Razorpay integration:** Payment support via `razorpay` package (see requirements.txt).
- **Session & Auth:** Uses Django's built-in authentication and session management.
- **Animations/UI:** Animations and dynamic UI (e.g., language toggle, card flip) are handled in template JS and CSS.

## Examples
- **Add a new page:**
  1. Create a view in `core/views.py`.
  2. Add a URL in `core/urls.py`.
  3. Create a template in `core/templates/core/`.
- **Add a static image:** Place in `core/static/images/` and reference in template: `{% static 'images/filename.png' %}`

## Key Files
- `manage.py`, `Agrokart/settings.py`, `core/views.py`, `core/urls.py`, `core/templates/core/home.html`, `requirements.txt`

---

If you add new conventions or workflows, update this file to help future AI agents and developers.
