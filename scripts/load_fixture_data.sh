#!/bin/bash

./manage.py loaddata ./news/fixtures/locations.json

./manage.py loaddata ./app/fixtures/auth.json
