#!/bin/sh

poetry run app & poetry run celery -A tasks worker -l info
