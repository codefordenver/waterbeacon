#!/bin/bash

# dump test data for app
./manage.py dumpdata app.location app.data --indent 4  > ./app/fixtures/test_data.json

# dump test data for news
./manage.py dumpdata news.advisory_feed news.advisory_keyword news.alert news.url news.utility news.county_served --indent 4  > ./news/fixtures/test_data.json

# dump raw data
./manage.py dumpdata rawdata.EpaFacilitySystem --indent 4 > ./rawdata/fixtures/facility_system.json
