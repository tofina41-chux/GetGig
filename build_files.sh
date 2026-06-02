#!/bin/bash
echo "==> Installing workspace dependencies..."
pip install -r requirements.txt

echo "==> Compiling server-level Django static assets..."
python manage.py collectstatic --noinput --clear