from datetime import datetime
import requests
import pandas as pd

class epa_sdwis(object):
    # REF: https://echo.epa.gov/tools/web-services/facility-search-drinking-water
    # SCORE Calc https://github.com/andersjr1984/dwCalculation/blob/master/wqCalc.js

    def __init__(self):
        self._host = 'iaspub.epa.gov'

    def _get(self, endpoint, headers={}, params={}, print_test=False):
        ''' executes get request '''
        url = "https://%s/%s" % (self._host, endpoint)

        headers = {
              'content-language': 'en',
              'content-type': 'application/json'
        }

        res = requests.get(url, params=params, headers = headers)

        if res.status_code == 200:
            return res.json()
        else:
            return res.json()

    def area_score(self, df):

        list = [
            {'zipcode': [{
                'facility_id': abc123,
                'pws_type_code': 'CWS',
                'facility_score': 0...1,
                'population_served': X
                }]
            }
        ]

        # sum of all facility scores in the zipcode include CWIS, NTNCWS + TNCWS

        # facility_score, population_served = facility_score()


    def zip_code_calc(self, list):

        # CWIS water score
        # if facility is CWS, it contributes to the CWS water score

        # sum all population served for CWIS

        # community_score = ( facility_score1 * pop_served1 + facility_score2 * pop_served2)  / sum total_population served


        # other water score
        # sum all population served for NTNCWS + TNCWS
        # other_score = ( facility_score1 * pop_served1 + facility_score2 * pop_served2)  / sum total_population served

        # community_score * 0.6 + other_score * 0.4

        # Edge case if either CWIS or OTHER is 0, return the max of both scores


    def facility_score(self, violations):
        # POPULATION_SERVED_COUNT
        # COMPLIANCE_STATUS_CODE
        # IS_MAJOR_VIOL_IND
        # PUBLIC_NOTIFICATION_TIER

        # every facility start with a score of 1

        # if No violations in the past X (3) years, return a score of 1

        # else if there are violtions and there is a status code of O, then they facility
        # subtracts 0.4 from score

        # .4 derived based on the weight of a community that current


        # the remaining is a historical score 0.6

        # count the violations, if there are more than 12 Quarters of violations or 3 years,
        # then they get a zero for the historical scores

        # less than 12 violations
        # violation_score = 0.6

        # iterate through each voilation

        # if violation is major or tier === 1
            # violation_score -= 0.6 * 1/12
        # elif tier === 2
            # violation_score -= 0.6 * 1/18
        # elif tier === 3
            # violation_score -= 0.6 * 1/24

        # return facility_score, pop_served



    def get_data(self, start_date = datetime(2013, 01, 01, 0, 0), start_row = 0, end_row = 10):

        endpoint = '/enviro/efservice/WATER_SYSTEM/PWS_ACTIVITY_CODE/=/A/VIOLATION/VIOLATION_ROW/COMPL_PER_BEGIN_DATE/>/%s/rows/%s:%s/JSON/' % ( start_date.strftime('%m-%b-%Y'), start_row, end_row  )

        data = self._get(endpoint)

        # insert data into pandas dataframe
        df = pd.DataFrame(data, index=['PHONE_NUMBER',
                                       'ADDRESS_LINE1',
                                       'EMAIL_ADDR',
                                       'ZIP_CODE',
                                       'CITY_NAME',
                                       'EPA_REGION',
                                       'PRIMACY_AGENCY_CODE',
                                       'POPULATION_SERVED_COUNT',
                                       'ORG_NAME',
                                       'PHONE_NUMBER',
                                       'STATE_CODE',
                                       'COUNTIES_SERVED',
                                       'COMPLIANCE_STATUS_CODE',
                                       'IS_MAJOR_VIOL_IND',
                                       'PUBLIC_NOTIFICATION_TIER',
                                       'PWSID',             # PWS: Public Water System
                                       'PWS_TYPE_CODE',
                                       'PWS_NAME'])

        for object in data:

        return data



if __name__ == "__main__":
    sdwis = epa_sdwis()

    print(sdwis.get_data())
