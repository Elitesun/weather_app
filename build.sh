#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Navigate to the directory containing manage.py
cd weather

python manage.py collectstatic --no-input
python manage.py migrate 

cd weather