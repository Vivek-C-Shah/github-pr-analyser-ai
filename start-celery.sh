#!/bin/sh

celery -A celery_app worker --loglevel=info --concurrency=1