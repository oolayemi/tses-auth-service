#!/bin/sh

celery -A core worker --loglevel=info --concurrency=2 --hostname=worker1@%h --detach

celery -A core beat -l INFO --detach
celery -A core beat -l INFO --detach --scheduler django_celery_beat.schedulers:DatabaseScheduler

exec "$@"
