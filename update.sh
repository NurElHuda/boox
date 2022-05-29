#!/usr/bin/env bash

git pull
pip3 install -r requirements.txt -q
python3 manage.py migrate
python3 manage.py collectstatic --noinput
