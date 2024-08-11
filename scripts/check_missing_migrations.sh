#!/bin/bash

# Check for missing migrations
python manage.py makemigrations --check --dry-run

# Capture the status code
status=$?

if [ $status -ne 0 ]; then
    echo "Error: There are changes in your models that are not reflected in migrations."
    echo "Please run 'python manage.py makemigrations' to create the necessary migrations."
    exit 1
fi

exit 0
