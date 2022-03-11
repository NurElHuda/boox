#!/usr/bin/env bash

export APP_NAME='boox_app'
source venv/bin/activate
python manage.py admin_generator $APP_NAME > $APP_NAME/admin.py