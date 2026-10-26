# Pixlo — Social Media Platform

A responsive social media starter built with HTML, CSS, JavaScript, Django, and PostgreSQL.

## Features
- Sign up, log in, and log out
- Feed with text/photo posts
- Like/unlike posts
- Add comments
- User profiles and follow/unfollow
- Edit your profile bio and avatar URL
- Search users
- Responsive mobile-friendly interface
- Django admin panel

## Requirements
- Python 3.10+
- PostgreSQL 13+
- pip

## 1. Create a PostgreSQL database
Open `psql` or pgAdmin and create a database and user. Example:

```sql
CREATE DATABASE pixlo_db;
CREATE USER pixlo_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE pixlo_db TO pixlo_user;
```

For PostgreSQL 15+, if migrations report permission errors, connect to `pixlo_db` as a database owner and run:
```sql
GRANT ALL ON SCHEMA public TO pixlo_user;
```

## 2. Set up the project
From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update the PostgreSQL credentials. On macOS/Linux:
```bash
cp .env.example .env
```

## 3. Run migrations and create an admin
```bash
python manage.py makemigrations social
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Notes
- PostgreSQL is configured through environment variables in `.env`.
- Uploaded post images are stored in `media/`.
- For production, set a strong `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`, use HTTPS, and serve static/media files correctly.
- This is a runnable starter project, not a fully hardened production service. Add automated tests, rate limiting, content moderation, email verification, and production media storage before launching publicly.
