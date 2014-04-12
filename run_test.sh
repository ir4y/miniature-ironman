#!/bin/bash
export PYTHONPATH=. 
export DJANGO_SETTINGS_MODULE=tests.settings
py.test --create-db
