#!/usr/bin/env bash
set -e

cd /home/django/project
docker exec -it django_1 python3 manage.py dumpdata --all --indent 4 --natural-primary --natural-foreign > /home/django/backups/dumpdata_$(date +"%Y-%m-%d").json
find /home/django/backups/* -mtime +30 -delete
