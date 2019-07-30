#!/usr/bin/env bash

set -o errexit
set -o nounset


celery flower \
    --app=cinema_city_clone.celery:app \
    --broker="${CELERY_BROKER_URL}"
