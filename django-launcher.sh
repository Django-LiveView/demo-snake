#!/bin/sh

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate


# Start server

echo "*****Start server with debug mode*****"
python3 manage.py runserver 0.0.0.0:8000

#echo "*****Start server with production mode*****"
#daphne -b 0.0.0.0 -p 8000 core.asgi:application
