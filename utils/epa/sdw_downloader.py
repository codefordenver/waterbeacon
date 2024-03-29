
from datetime import datetime
import requests
import json
import csv
import os
import time


class EpaDataGetter(object):

    WATER_TYPE = 'WaterSystems'
    FACILITY_TYPE = 'Facilities'
    VALID_REQUEST_TYPES = (WATER_TYPE, FACILITY_TYPE)

    def __init__(self, requests_before_pause=3, pause_seconds=3):
        self.hostname = 'https://echodata.epa.gov/echo'

        # the system rate limits and this is crude without a nice retry system
        self.requests_before_pause = requests_before_pause
        self.pause_seconds = pause_seconds
        self.request_count = 0
        self.request_type = ''
        self.system_url = ''
        self.query_url = ''
        self.desired_columns = ()  # Iterable of column names
        self.endpoint_metadata_url = ''
        self.columns_query_param = ''
        self.failed_requests = []
        self.get_queryid_request_parameters = ''

        self.states = [
            "AL",  "AK",  "AS",  "AZ",  "AR",  "CA",  "CO",  "CT",
            "DE",  "DC",  "FM",  "FL",  "GA",  "GU",  "HI",  "ID",
            "IL",  "IN",  "IA",  "KS",  "KY",  "LA",  "ME",  "MH",
            "MD",  "MA",  "MI",  "MN",  "MS",  "MO",  "MT",  "NE",
            "NV",  "NH",  "NJ",  "NM",  "NY",  "NC",  "ND",  "MP",
            "OH",  "OK",  "OR",  "PW",  "PA",  "PR",  "RI",  "SC",
            "SD",  "TN",  "TX",  "UT",  "VT",  "VI",  "VA",  "WA",
            "WV", "WI",  "WY"
        ]

    def collect_and_save_data(self, output_directory):
        if self.request_type not in EpaDataGetter.VALID_REQUEST_TYPES:
            raise ValueError(
                'Invalid request type. Must be watersystem or facility.')

        for state in self.states:
            self._get_query_id_from_epa_system_url(state)
            if self.query_id is None:
                continue
            file_name = '%s.csv' % state
            target_file = os.path.join(
                output_directory, self.request_type, file_name)
            self._create_target_file(target_file)
            data, page = True, 1
            while data:
                data = self._get_page_of_data_for_query_id(page)
                page += 1
                if data is not None:
                    self._append_data_to_file(data, target_file)

    def get_column_url_parameters_from_metadata(self):
        if not (self.desired_columns and self.endpoint_metadata_url):
            raise ValueError(
                'Missing required values: self.desired_columns or self.endpoint_metadata_url')
        data = self._get_json_data_from_url(self.endpoint_metadata_url)
        query_params = ''
        missing_columns = False
        missing_columns_list = []
        for col in self.desired_columns:
            col_info = [d
                        for d in data['Results']['ResultColumns'] if d['ColumnName'] == col]
            if col_info:
                column_id = col_info[0]['ColumnID']
                if query_params:
                    # %2C is a comma
                    query_params += '%2C{!s}'.format(column_id)
                else:
                    query_params += '{!s}'.format(column_id)
            else:
                print('missing %s' % col)
                missing_columns_list.append(col)
                missing_columns = True
        if missing_columns:
            raise ValueError('Missing columns: %s' % missing_columns_list)
        return '&qcolumns=%s' % query_params

    def _create_target_file(self, target_file):
        with open(target_file, 'w'):
            pass  # just open the file to delete everything

    def _should_write_row(self, row):
        return True

    def _append_data_to_file(self, data, target_csv):
        with open(target_csv, 'a') as f:
            csvwriter = csv.writer(f)
            count = 0
            previous_data = os.stat(target_csv).st_size != 0
            for row in data:
                if not previous_data and count == 0:
                    header = row.keys()
                    csvwriter.writerow(header)
                    count += 1
                if self._should_write_row(row):
                    csvwriter.writerow(row.values())

    def _get_page_of_data_for_query_id(self, page_number):
        """
        It turns out the download endpoints are not thorough enough so we need to use the paginated data.
        The assummptions about query parameter names hopefully holds true for all endpoints like it has so far.
        """
        self._rate_limit_requests()
        url = '%s?output=JSON&qid=%s&pageno=%s%s' % (
            self.query_url, self.query_id, page_number, self.columns_query_param)
        # self.stdout.write(url) # not available unless this is in a command
        # should try/except here to handle timeouts, over hitting API
        print(url)
        data = self._get_json_data_from_url(url)
        # returns an empty array when past last page of data. It doesn't seem the API otherwise indicates??
        if not data["Results"]:
            return None
        elif not data["Results"][self.request_type]:
            return None
        else:
            return data["Results"][self.request_type]

    def _reset_query_results(self):
        self.query_id = None
        self.query_rows = None

    def _rate_limit_requests(self):
        self.request_count += 1
        if self.request_count % self.requests_before_pause == 0:
            time.sleep(self.pause_seconds)

    def _get_json_data_from_url(self, url):
        raw_json = requests.get(url)
        if raw_json.status_code == 200:
            try:
                data = json.loads(raw_json.content)
            except UnicodeDecodeError:
                # if this ever fails, we could do something like try
                # encoding = raw_json.encoding or raw_json.apparent_encoding or 'ISO-8859-1'
                data = json.loads(raw_json.content.decode('ISO-8859-1'))
        else:
            raise ValueError('Invalid response: %s %s' %
                             (raw_json.status_code, raw_json.content))
        return data

    def _get_query_id_from_epa_system_url(self, state):
        """
        This expects an EPA endpoint that returns a query ID so we can then process the data separately.
        Just setting the property rather than returning a value but that feels weird.
        The assummption about query parameter names hopefully holds true for all endpoints like it has so far.
        """
        self._rate_limit_requests()
        url = '%s?output=JSON&p_st=%s&p_act=Y%s' % (
            self.system_url, state, self.get_queryid_request_parameters)
        print(url)
        data = self._get_json_data_from_url(url)
        print(data)
        try:
            data = data["Results"]
            query_rows = int(data["QueryRows"])
            query_id = data["QueryID"]
            if query_rows != 0 and query_id:
                self.query_id = query_id
                self.query_rows = query_rows
            else:
                self._reset_query_results()
                return
        except KeyError:
            self._reset_query_results()
            self.failed_requests.append((state, url))
            return


class EpaFacilityDataGetter(EpaDataGetter):

    def __init__(self):
        super(EpaFacilityDataGetter, self).__init__()
        self.request_type = EpaDataGetter.FACILITY_TYPE
        self.system_url = '%s/echo_rest_services.get_facilities' % self.hostname
        self.query_url = '%s/echo_rest_services.get_qid' % self.hostname
        self.endpoint_metadata_url = '%s/echo_rest_services.metadata?output=JSON' % self.hostname
        self.desired_columns = ('REGISTRY_ID', 'FAC_NAME', 'SDWA_IDS', 'FAC_STREET', 'FAC_CITY', 'FAC_STATE', 'FAC_ZIP', 'FAC_COUNTY', 'FAC_FIPS_CODE', 'FAC_DERIVED_ZIP', 'FAC_EPA_REGION', 'FAC_LAT', 'FAC_LONG', 'FAC_ACCURACY_METERS', 'FAC_REFERENCE_POINT', 'FAC_TOTAL_PENALTIES', 'FAC_DATE_LAST_PENALTY', 'FAC_LAST_PENALTY_AMT', 'SDWA_FORMAL_ACTION_COUNT',
                                'SDWA_SYSTEM_TYPES', 'FAC_DERIVED_STCTY_FIPS', 'FAC_PERCENT_MINORITY', 'FAC_MAJOR_FLAG', 'VIOL_FLAG', 'CURR_VIO_FLAG', 'FAC_PENALTY_COUNT', 'FAC_FORMAL_ACTION_COUNT', 'SDWA_3YR_COMPL_QTRS_HISTORY', 'SDWA_INSPECTIONS_5YR', 'SDWA_INFORMAL_COUNT', 'FAC_COLLECTION_METHOD', 'FAC_STD_COUNTY_NAME', 'SDWIS_FLAG', 'FAC_IMP_WATER_FLG', 'SCORE')
        self.columns_query_param = self.get_column_url_parameters_from_metadata()
        # filter for water only facilities
        self.get_queryid_request_parameters = '&p_med=S'

    def should_write_row(self, row):
        # Indicates whether the facility has a Safe Drinking Water Information System (SDWIS) ID
        # We don't care about any facilities that aren't water related (could look for watershed info someday)
        # Figured out parameter for this so it should probably be removed
        return row["SDWISFlag"] == 'Y'


class EpaWaterDataGetter(EpaDataGetter):

    def __init__(self):
        super(EpaWaterDataGetter, self).__init__()
        self.request_type = EpaDataGetter.WATER_TYPE
        self.system_url = '%s/sdw_rest_services.get_systems' % self.hostname
        self.query_url = '%s/sdw_rest_services.get_qid' % self.hostname
        # maybe we want to restrict the data in this case too but we can just store it all in the meantime
        # self.endpoint_metadata_url = '%s/sdw_rest_services.metadata?output=JSON' % self.hostname
        # self.desired_columns = ()
        # self.columns_query_param = self.get_column_url_parameters_from_metadata()
        # for water locations, we also use the numeric codes that are typically reservations. probably unnecesary as the state should have duplicate info
        self.states.append(('01',  '02',  '03',  '04',  '05',
                            '06',  '07',  '08', '09',  '10'))


class SDW_Downloader(object):

    def __init__(self):
        pass

    def get_facility_data(self, target_dir):
        facility_getter = EpaFacilityDataGetter()
        facility_getter.collect_and_save_data(target_dir)

    def get_water_data(self, target_dir):
        water_getter = EpaWaterDataGetter()
        water_getter.collect_and_save_data(target_dir)
