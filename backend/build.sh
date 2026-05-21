#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py compilemessages
python manage.py collectstatic --noinput --clear --verbosity 2
python manage.py migrate

python manage.py seed_db || true
python manage.py seed_exercises || true
python manage.py seed_blog || true
python manage.py seed_badges || true
python manage.py seed_recipes || true
python manage.py seed_programs || true
python manage.py seed_shop || true
python manage.py seed_demo_user || true
