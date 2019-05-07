from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
import json
import os
import time


states = [
    '01',  '02',  '03',  '04',  '05',  '06',  '07',  '08',
    '09',  '10',
    "AL",  "AK",  "AS",  "AZ",  "AR",  "CA",  "CO",  "CT",
    "DE",  "DC",  "FM",  "FL",  "GA",  "GU",  "HI",  "ID",
    "IL",  "IN",  "IA",  "KS",  "KY",  "LA",  "ME",  "MH",
    "MD",  "MA",  "MI",  "MN",  "MS",  "MO",  "MT",  "NE",
    "NV",  "NH",  "NJ",  "NM",  "NY",  "NC",  "ND",  "MP",
    "OH",  "OK",  "OR",  "PW",  "PA",  "PR",  "RI",  "SC",
    "SD",  "TN",  "TX",  "UT",  "VT",  "VI",  "VA",  "WA",
    "WV",  "WI",  "WY"
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for state in states:
            self.state = state
            self.stdout.write('Getting data for %s' % self.state)  # TODO add verbose logging control
            self.get_state_data()


    def get_state_data(self):
        requestUrl = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_systems?output=JSON&p_st=%s&p_act=Y' % self.state
        data = get_json_data_from_url(requestUrl)
        self.query_id = data["Results"]["QueryID"]
        if self.query_id:
            print('%s qid=%s' % (self.state, self.query_id))
            self.get_and_save_facility_data_for_state()
            # yeah, sleeping sux but it sounds like they have rate limits. should be able to make it through state np
            #TODO add a backoff so we don't have to sleep
            time.sleep(1)


    def get_and_save_facility_data_for_state(self):
        proceed = True
        page_number = 0
        while proceed is True:
            page_number += 1  # page 0 doesn't include data
            url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_qid?output=JSON&qid=%s&pageno=%s' % (self.query_id, page_number)
            self.stdout.write(url)
            # should try/except here to handle timeouts, over hitting API
            data = get_json_data_from_url(url)
            # returns an empty array when past last page of data
            if not data["Results"]["WaterSystems"]:
                proceed = False
                break
            file_name = '%spage%s.json' % (self.state, page_number)
            target_file = os.path.join(settings.BASE_DIR, settings.EPA_STATE_DATA_DIRECTORY ,file_name)
            self.stdout.write('Writing file %s' % file_name)
            save_json_data_to_file(data, target_file)


def get_json_data_from_url(url):
    raw_json = requests.get(url)
    if raw_json.status_code == 200:
        data = json.loads(raw_json.content)
    else:
        raise ValueError('Invalid response: %s %s' %
                        (raw_json.status_code, raw_json.content))
    return data


def save_json_data_to_file(json_data, target_file):
    with open(target_file, 'w') as f:
        f.write(json.dumps(json_data))
