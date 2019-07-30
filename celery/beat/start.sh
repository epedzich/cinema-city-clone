#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

rm -f './celerybeat.pid'
watchmedo auto-restart --directory=./ --pattern=tasks.py;settings.py --recursive -- celery -A cinema_city_clone.celery:app beat -l INFO
