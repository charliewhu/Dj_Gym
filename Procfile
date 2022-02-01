release: python manage.py migrate
release: python manage.py loaddata rir.json
web: gunicorn web_project.wsgi