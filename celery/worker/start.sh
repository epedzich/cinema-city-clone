#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A cinema_city_clone.celery:app worker -l INFO
