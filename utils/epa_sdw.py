import requests
import pandas as pd

class epa_sdw(object):

    def __init__(self):
        self.host = 'ofmpub.epa.gov'

    def _get(self, endpoint, headers={}, params={}, print_test=False):
        ''' executes get request '''
        url = "https://%s/%s" % (self._host, endpoint)

        res = requests.get(url, params=params, headers = headers)

        if res.status_code == 200:
            return res.json()
        else:
            return res.json()

    def _get_systems(self):
        endpoint = '/echo/sdw_rest_services.get_systems'
        params = {
            'p_fips':fips
        }
        self.get(endpoint, params = params)

    def _get_quid(self, qid, page):
        endpoint = '/echo/sdw_rest_services.get_qid'
        params = {
            'qid':qid,
            'page': page
        }

        self.get(endpoint, params = params)


    def get_data(self, fips):

        # Returns an array of public water systems that meet the specified search criteria.
        systems = self._get_systems(fips)

        # this request returns the systems detail containing all matching water systems
        systems_detail = self._get_quid()
