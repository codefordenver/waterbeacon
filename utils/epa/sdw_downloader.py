
from datetime import datetime
import requests
import json
import csv
import os
import time
import zipfile
import timeit


class FileDownloader():

    def __init__(self):
        pass

    def download_file(self, download_url, target_file):
        start_time = timeit.default_timer()
        # this relies on the folder that the file is in existing
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(target_file, 'wb') as f:
                # tested 65592 and it was worse
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        elapsed = timeit.default_timer() - start_time
        print('took %s seconds to download the file' %
              elapsed)  # TODO use stdout


class ZipDataDownloader():

    def __init__(self, download_url, target_dir, target_zip_file):
        # should this be inherited? passed in DI style?
        self.file_downloader = FileDownloader()
        self._download_url = download_url
        self._target_dir = target_dir
        self._target_zip = os.path.join(target_dir, target_zip_file)

    def extract_zip_data_to_file(self):
        # There are recommendations against extracting all from internet sources.
        # This assumes that it's safe to do so
        with zipfile.ZipFile(self._target_zip, 'r') as zf:
            for info in zf.infolist():
                zf.extract(info, self._target_dir)

    def download_and_extract_file(self):
        self.file_downloader.download_file(
            self._download_url, self._target_zip)
        self.extract_zip_data_to_file()


class FullFacilityDownloader():

    IS_ACTIVE_COL_NAME = 'FAC_ACTIVE_FLAG'
    IS_WATER_FAC_COL_NAME = 'SDWIS_FLAG'
    WATER_SYSTEM_TYPE_COL_NAME = 'SDWA_SYSTEM_TYPES'
    SDWA_IDS_COL_NAME = 'SDWA_IDS'
    CWS_IDENTIFIER = 'Community water system'

    def __init__(self, target_dir):
        self.full_facility_file = os.path.join(target_dir, 'ECHO_EXPORTER.csv')
        self._target_dir = target_dir
        self._downloader = ZipDataDownloader('https://echo.epa.gov/files/echodownloads/echo_exporter.zip',
                                             target_dir, 'echo_exporter.zip')

    def _write_row(self, target_file, csv_row):
        target_file.write('%s\n' % ','.join(csv_row))

    def _get_row_value(self, column_name):
        return self.row[self._csv_columns.index(column_name)]

    def _set_row_value(self, row, column_name, new_value):
        row[self._csv_columns.index(column_name)] = new_value
        return row

    def _get_dedicated_pws_rows_for_facility(self):
        result_rows = []
        sdwa_ids = self._get_row_value(self.SDWA_IDS_COL_NAME).split(' ')
        system_types = self._get_row_value(
            self.WATER_SYSTEM_TYPE_COL_NAME).split(',')
        if len(sdwa_ids) > 1:
            for i, pws_id in enumerate(sdwa_ids):
                row = self.row.copy()  # we don't want to mutate the shared list copy
                row[self._csv_columns.index(self.SDWA_IDS_COL_NAME)] = pws_id
                # 1-1 between system and type so we match values. if different, just leave it alone because it's confusing
                if len(system_types) == len(sdwa_ids):
                    row[self._csv_columns.index(
                        self.WATER_SYSTEM_TYPE_COL_NAME)] = system_types[i]
                result_rows.append(row)
        else:
            result_rows.append(self.row)
        return result_rows

    def extract_water_facilities_to_file(self, target_water_csv, download_facility_extract=True) -> str:
        """
        optionally downloads the ECHO export, then extracts active SDWA facilities to a csv and 
        returns the path to the file. this only includes active community water systems in the output
        """
        self.final_water_csv = os.path.join(self._target_dir, target_water_csv)

        # for now, no reason to expose this download file on own, just expose the 'processed' version
        if download_facility_extract:
            self._downloader.download_and_extract_file()

        first_row = True
        with open(self.final_water_csv, 'w') as target:
            with open(self.full_facility_file, newline='\n') as f:
                facilityreader = csv.reader(f, delimiter=',', quotechar='"')
                for row in facilityreader:
                    self.row = row
                    if first_row:
                        self._csv_columns = row
                        first_row = False
                        self._write_row(target, row)
                    else:
                        active = self._get_row_value(
                            self.IS_ACTIVE_COL_NAME) == 'Y'
                        is_water_facility = self._get_row_value(
                            self.IS_WATER_FAC_COL_NAME) == 'Y'
                        # using contains here because facility does not map 1-1 with water systems
                        # see e.g. 110010194814 for SDWA_IDS: 'PA2450056 PA2450127 PA2450128'
                        # also note that all PWS IDs can be the same type, or not, but the data isn't very clear about it
                        # SDWA_IDS are split by spaces and the system types are split by commas, and they don't map 1-1, cause duh
                        contains_community_water_system = self.CWS_IDENTIFIER in self._get_row_value(
                            self.WATER_SYSTEM_TYPE_COL_NAME)
                        if (active and is_water_facility and contains_community_water_system):
                            rows = self._get_dedicated_pws_rows_for_facility()
                            for r in rows:
                                self._write_row(target, r)

        return self.final_water_csv


class EpaDataGetter(object):

    WATER_TYPE = 'WaterSystems'
    FACILITY_TYPE = 'Facilities'
    VALID_REQUEST_TYPES = (WATER_TYPE, FACILITY_TYPE)

    def __init__(self, systems_query_url='', results_by_qid_query_url='', results_by_download_query_url='', desired_columns=(), endpoint_metadata_url='',
                 request_type='', requests_before_pause=3, pause_seconds=3):
        """
        you pass the original systems_query_url to get your query ID which is then used by either of the results_by_*_url to 
        get a download of the results or to iterate through the results by page
        """
        self.requests_before_pause = requests_before_pause
        self.pause_seconds = pause_seconds
        self.request_type = request_type
        self.get_systems_url = systems_query_url
        self.by_qid_query_url = results_by_qid_query_url
        self.by_download_query_url = results_by_download_query_url

        self.failed_requests = []
        self.request_count = 0
        self.file_downloader = FileDownloader()

        if desired_columns and endpoint_metadata_url:
            self.columns_query_param = self.get_column_url_parameters_from_metadata(
                desired_columns, endpoint_metadata_url)

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

    def _add_query_params(self, base_url, query_params):
        if '?' in base_url:
            url = base_url + '&' + query_params
        else:
            url = base_url + '?' + query_params
        return url

    # this should be something like 'by_get_qid'
    def collect_and_save_data_by_states(self, output_directory):
        if self.request_type not in EpaDataGetter.VALID_REQUEST_TYPES:
            raise ValueError(
                'Invalid request type. Must be watersystem or facility.')

        for state in self.states:
            # ish, this url manipulation is bad bad not good
            query_params = 'output=JSON&p_st=%s' % state
            url = self._add_query_params(self.get_systems_url, query_params)
            self._set_query_id_from_epa_search_url(url)
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

    def collect_and_save_data_by_get_download(self, target_file):
        search_url = self._add_query_params(
            self.get_systems_url, 'output=JSON')
        self._set_query_id_from_epa_search_url(search_url)
        download_url = self._add_query_params(
            self.by_download_query_url, query_params='qid=%s&%s' % (self.query_id, self.columns_query_param))
        print(download_url)
        self.file_downloader.download_file(download_url, target_file)

    def get_column_url_parameters_from_metadata(self, desired_columns, endpoint_metadata_url):
        if not (desired_columns and endpoint_metadata_url):
            raise ValueError(
                'Missing required values: self.desired_columns or self.endpoint_metadata_url')
        if not 'output' in endpoint_metadata_url:
            endpoint_metadata_url = self._add_query_params(
                endpoint_metadata_url, 'output=JSON')
        data = self._get_json_data_from_url(endpoint_metadata_url)
        column_query_params = ''
        missing_columns = False
        missing_columns_list = []
        for col in desired_columns:
            col_info = [d
                        for d in data['Results']['ResultColumns'] if d['ColumnName'] == col]
            if col_info:
                column_id = col_info[0]['ColumnID']
                if column_query_params:
                    # %2C is a comma
                    column_query_params += '%2C{!s}'.format(column_id)
                else:
                    column_query_params += '{!s}'.format(column_id)
            else:
                print('missing %s' % col)
                missing_columns_list.append(col)
                missing_columns = True
        if missing_columns:
            raise ValueError('Missing columns: %s' % missing_columns_list)
        return 'qcolumns=%s' % column_query_params

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
        url = self._add_query_params(self.by_qid_query_url, query_params='output=JSON&qid=%s&pageno=%s&%s' % (
            self.query_id, page_number, self.columns_query_param))
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

    def _set_query_id_from_epa_search_url(self, url):
        """
        This expects an EPA endpoint that returns a query ID so we can then process the data separately.
        Just setting the property rather than returning a value but that feels weird.
        The assummption about query parameter names hopefully holds true for all endpoints like it has so far.
        """
        self._rate_limit_requests()

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
            self.failed_requests.append(url)
            return

# region Old extract classes


class EpaFacilityDataGetter(EpaDataGetter):

    def __init__(self):
        get_systems_url = 'https://ofmpub.epa.gov/echo/echo_rest_services.get_facilities?p_act=Y&p_med=S'
        by_qid_query_url = 'https://ofmpub.epa.gov/echo/echo_rest_services.get_qid'
        endpoint_metadata_url = 'https://ofmpub.epa.gov/echo/echo_rest_services.metadata'
        desired_columns = ('REGISTRY_ID', 'FAC_NAME', 'SDWA_IDS', 'FAC_STREET', 'FAC_CITY', 'FAC_STATE', 'FAC_ZIP', 'FAC_COUNTY', 'FAC_FIPS_CODE', 'FAC_DERIVED_ZIP', 'FAC_EPA_REGION', 'FAC_LAT', 'FAC_LONG', 'FAC_ACCURACY_METERS', 'FAC_REFERENCE_POINT', 'FAC_TOTAL_PENALTIES', 'FAC_DATE_LAST_PENALTY', 'FAC_LAST_PENALTY_AMT', 'SDWA_FORMAL_ACTION_COUNT',
                           'SDWA_SYSTEM_TYPES', 'FAC_DERIVED_STCTY_FIPS', 'FAC_PERCENT_MINORITY', 'FAC_MAJOR_FLAG', 'VIOL_FLAG', 'CURR_VIO_FLAG', 'FAC_PENALTY_COUNT', 'FAC_FORMAL_ACTION_COUNT', 'SDWA_3YR_COMPL_QTRS_HISTORY', 'SDWA_INSPECTIONS_5YR', 'SDWA_INFORMAL_COUNT', 'FAC_COLLECTION_METHOD', 'FAC_STD_COUNTY_NAME', 'SDWIS_FLAG', 'FAC_IMP_WATER_FLG', 'SCORE')
        super().__init__(get_systems_url=get_systems_url, by_qid_query_url=by_qid_query_url, desired_columns=desired_columns,
                         endpoint_metadata_url=endpoint_metadata_url, request_type=EpaDataGetter.FACILITY_TYPE)

    def should_write_row(self, row):
        # Indicates whether the facility has a Safe Drinking Water Information System (SDWIS) ID
        # We don't care about any facilities that aren't water related (could look for watershed info someday)
        # Figured out parameter for this so it should probably be removed
        return row["SDWISFlag"] == 'Y'


class EpaWaterDataGetter(EpaDataGetter):

    def __init__(self):
        by_qid_query_url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_qid'
        get_systems_url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_systems'
        super().__init__(system_url=get_systems_url,
                         by_qid_query_url=by_qid_query_url, request_type=EpaDataGetter.WATER_TYPE)

# endregion


class EpaWaterDataGetterGood(EpaDataGetter):

    def __init__(self):
        get_systems_url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_systems?p_act=Y&p_systyp=CWS'
        by_download_query_url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.get_download'
        endpoint_metadata_url = 'https://ofmpub.epa.gov/echo/sdw_rest_services.metadata'
        desired_columns = ('PWS_NAME', 'PWSID', 'CITIES_SERVED', 'STATE_CODE', 'ZIP_CODES_SERVED',
                           'COUNTIES_SERVED', 'EPA_REGION', 'INDIAN_COUNTRY', 'PWS_TYPE_CODE', 'PWS_TYPE_DESC', 'PRIMARY_SOURCE_CODE',
                           'PRIMARY_SOURCE_DESC', 'POPULATION_SERVED_COUNT', 'PWS_ACTIVITY_CODE', 'PWS_ACTIVITY_DESC', 'QTRS_WITH_VIO',
                           'QTRS_WITH_SNC', 'SERIOUS_VIOLATOR', 'HEALTH_FLAG', 'MR_FLAG', 'PN_FLAG', 'OTHER_FLAG', 'NEW_VIO_FLG',
                           'RULES_VIO_3YR', 'RULES_VIO', 'VIOPACCR', 'VIOREMAIN', 'VIOFEANOT', 'VIORTCFEA', 'VIORTCNOFEA', 'IFEA',
                           'FEAS', 'SDW_DATE_LAST_IEA', 'SDW_DATE_LAST_IEA_EPA', 'SDW_DATE_LAST_IEA_ST', 'SDW_DATE_LAST_FEA',
                           'SDW_DATE_LAST_FEA_EPA', 'SDW_DATE_LAST_FEA_ST', 'SDWA_CONTAMINANTS_IN_VIOL_3YR', 'SDWA_CONTAMINANTS_IN_CUR_VIOL',
                           'FIPS_CODES', 'SDWA_3YR_COMPL_QTRS_HISTORY', 'SDWA_CONTAMINANTS', 'TRIBAL_FLAG', 'FEA_FLAG',
                           'IEA_FLAG', 'SNC_FLAG', 'CURR_VIO_FLAG', 'VIO_FLAG', 'INSP_5YR_FLAG', 'SERVICE_AREA_TYPE_CODE',
                           'SERVICE_AREA_TYPE_DESC', 'VIOLATION_CATEGORIES', 'SANSURVEY5YR', 'DATE_LAST_SANSURVEY',
                           'SIGNIFICANT_DEFICIENCY_COUNT', 'SIGNIFICANT_DEFICIENCY_COUNT_ILS', 'SDW_DATE_LAST_VISIT',
                           'SDW_DATE_LAST_VISIT_EPA', 'SDW_DATE_LAST_VISIT_STATE', 'SDW_DATE_LAST_VISIT_LOCAL', 'SITE_VISITS_5YR_ALL',
                           'SITE_VISITS_5YR_INSPECTIONS', 'SITE_VISITS_5YR_OTHER', 'REGISTRY_ID')

        super().__init__(get_systems_url=get_systems_url, by_download_query_url=by_download_query_url, desired_columns=desired_columns,
                         endpoint_metadata_url=endpoint_metadata_url, request_type=EpaDataGetter.WATER_TYPE)


class SDW_Downloader(object):

    def __init__(self):
        pass

    def get_facility_data(self, target_dir):
        facility_getter = EpaFacilityDataGetter()
        facility_getter.collect_and_save_data_by_states(target_dir)

    def get_water_data(self, target_dir):
        water_getter = EpaWaterDataGetter()
        water_getter.collect_and_save_data_by_states(target_dir)

    def get_facility_data_new(self, target_dir, download_file=True):
        facility_getter = FullFacilityDownloader(target_dir)
        csv = facility_getter.extract_water_facilities_to_file(
            'water_facilities.csv', download_facility_extract=download_file)

    def get_water_data_new(self, target_dir):
        water_getter = EpaWaterDataGetterGood()
        target_file = os.path.join(target_dir, 'water_data.csv')
        water_getter.collect_and_save_data_by_get_download(target_file)


if __name__ == "__main__":
    d = SDW_Downloader()
    target = '/Users/david/Downloads/test' # TODO fill this in from command line/env vars?
    d.get_facility_data_new(True)
    d.get_water_data_new()
