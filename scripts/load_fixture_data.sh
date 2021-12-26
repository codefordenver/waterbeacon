#!/bin/bash

./manage.py loaddata ./news/fixtures/locations.json

# admin test login
# u: admin@admin.com
# p: commonpassword
./manage.py loaddata ./app/fixtures/auth.json
