# update data
./manage.py download_epa_facility_data
./manage.py download_epa_water_data
./manage.py import_epa_facility_data
./manage.py import_epa_water_data

# calculate score
./manage.py data_cruncher
