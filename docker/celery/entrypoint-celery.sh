#!/bin/sh

set -ex

# Start Celery worker
celery -A core worker --loglevel=info  --pool=solo

exec "$@"
