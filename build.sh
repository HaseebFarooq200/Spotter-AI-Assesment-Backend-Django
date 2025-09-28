#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py makemigrations
python manage.py makemigrations spotter_AI_app

python manage.py migrate

