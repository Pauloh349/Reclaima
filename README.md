# Reclaima (local development)

This Django project is a lost & found prototype. Below are quick steps to run it locally.

Prerequisites

- Python 3.11+ (project was tested with Python 3.13)
- pip

Setup

1. Create a virtual environment and activate it (PowerShell):

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```pwsh
python -m pip install -r requirements.txt
# If requirements.txt is not present, at minimum install Pillow:
python -m pip install Pillow
```

3. Apply migrations and load demo data:

```pwsh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata lostfound/fixtures/demo_data.json
```

4. Create a superuser to access the admin:

```pwsh
python manage.py createsuperuser
```

5. Run the development server:

```pwsh
python manage.py runserver
```

6. Open the site:

- Home: http://127.0.0.1:8000/
- Lost items: http://127.0.0.1:8000/lost_items/
- Found items: http://127.0.0.1:8000/found/
- Report lost: http://127.0.0.1:8000/report/lost/
- Report found: http://127.0.0.1:8000/report/found/
- Admin: http://127.0.0.1:8000/admin/

Notes

- Uploaded images are saved to the `media/` directory and served automatically during development (when `DEBUG = True`).
- The forms limit image uploads to 5 MB and require an image MIME type.

If you'd like, I can:

- Add `requirements.txt` listing dependencies.
- Add thumbnail generation for uploaded images.
- Improve front-end form styling and client-side validation.
