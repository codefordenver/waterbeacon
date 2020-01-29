from app import models as app_models
from rawdata import models as rawdata_models
from app import models as app_models
from utils.log import log
import pandas as pd

class SDW_Data_Cruncher(object):


    # major violation for each of the last 12 quarters
    _HISTORICAL_MAX_SCORE = 120.0

    # maxium score for a quartor
    _CURRENT_MAX_SCORE = 10.0

    _HISTORICAL_SCORE_WEIGHT = 0.4
    _CURRENT_SCORE_WEIGHT = 0.6

    _COMMUNITY_WATER_SYSTEM_WEIGHT = 0.6
    _OTHER_WATER_SYSTEM_WEIGHT = 0.4

    def __init__(self):
        pass

    def _calc_historical_score(self, viopaccr):
        # viopaccr: historical score
        if (viopaccr >= self._HISTORICAL_MAX_SCORE):
            # 1 represents the highest value which equates to the worst water quality in general
            return 1

        return viopaccr / self._HISTORICAL_MAX_SCORE

    def _calc_current_score(self, vioremain):
        # vioremain current score
        if (vioremain >= self._CURRENT_MAX_SCORE ):
            return 1

        return vioremain / self._CURRENT_MAX_SCORE

    def _calc_facility_score(self, facility):
        historical_score = self._calc_historical_score(facility['Viopaccr'])
        current_score = self._calc_current_score(facility['Vioremain'])
        population_served = facility['PopulationServedCount']
        unweighted_score = (historical_score + current_score) * population_served
        if (facility['PWSTypeCode'] == 'CWS'):
            return unweighted_score * self._COMMUNITY_WATER_SYSTEM_WEIGHT
        return unweighted_score * self._OTHER_WATER_SYSTEM_WEIGHT

    def _calc_area_score(self, state):
        systems = rawdata_models.EpaWaterSystem.objects.filter(StateCode = state).values()
        if systems.count() == 0:
            return pd.DataFrame([])
        
        systems_df = pd.DataFrame(list(systems))
        systems_df['FIPSCodes'].fillna(0, inplace = True)
        # this only takes the first listed value in FIPSCodes
        # can potentially change it to take all values and split into new rows
        systems_df['FIPSCodes'] = systems_df['FIPSCodes'].str.split(',', expand = True)[0]
        systems_df['Viopaccr'].fillna(0, inplace = True)
        systems_df['Vioremain'].fillna(0, inplace = True)
        systems_df['facility_weighted_score'] = systems_df.apply(lambda x: self._calc_facility_score(x), axis = 1)
        systems_df['IsCommWaterSystem'] = systems_df['PWSTypeCode'] == 'CWS'

        # sum the populations and weighted scores
        fips_populations = systems_df.groupby(['FIPSCodes', 'IsCommWaterSystem'])['PopulationServedCount'].sum()
        fips_weighted_scores = systems_df.groupby(['FIPSCodes', 'IsCommWaterSystem'])['facility_weighted_score'].sum()
        # combine values into one dataframe
        fips_info = pd.concat([fips_populations, fips_weighted_scores], axis = 1).reset_index()
        # evaluate adjusted score by dividing score by total population served
        fips_info['score'] = fips_info['facility_weighted_score'] / fips_info['PopulationServedCount']
        # this holds the accumulated scores for each FIPs code in a state
        fips_scores = fips_info.groupby('FIPSCodes')['score'].sum().reset_index()
        return fips_scores

    def calc_state_scores(self, state, print_test = False):
        if print_test:
            log('state: %s' % (state), 'success')

        areas = []
        for location in app_models.location.objects.filter(state = state).exclude(fips_county = ''):
            areas.append({
                'county_fips': location.fips_county
            })
        if len(areas) == 0:
            return pd.DataFrame(areas)
        area_info = pd.DataFrame(areas)
        area_scores = self._calc_area_score(state)

        area_df = pd.merge(area_scores, area_info, left_on='FIPSCodes', right_on='county_fips', how='right')
        area_df['score'].fillna(0, inplace=True)
        return area_df
