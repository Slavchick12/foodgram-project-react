run:
	python manage.py collectstatic
	python manage.py migrate
	gunicorn foodgram.wsgi --bind 0:8000
