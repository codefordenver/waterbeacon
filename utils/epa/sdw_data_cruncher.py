from app import models as app_models
from rawdata import models as rawdata_models
from app import models as app_models
from utils.log import log
from django_pandas.io import read_frame
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
            return 1 * self._HISTORICAL_SCORE_WEIGHT

        return (viopaccr / self._HISTORICAL_MAX_SCORE) * self._HISTORICAL_SCORE_WEIGHT

    def _calc_current_score(self, vioremain):
        # vioremain current score
        if (vioremain >= self._CURRENT_MAX_SCORE ):
            return 1 * self._CURRENT_SCORE_WEIGHT

        return (vioremain / self._CURRENT_MAX_SCORE) * self._CURRENT_SCORE_WEIGHT

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
        facilities = rawdata_models.EpaFacilitySystem.objects.filter(FacState = state).values()
        if systems.count() == 0 or facilities.count() == 0:
            return pd.DataFrame([])
        
        systems_df = read_frame(systems)
        systems_df = systems_df[['PWSId', 'FIPSCodes', 'Viopaccr', 'Vioremain', 'PopulationServedCount', 'PWSTypeCode']]
        fac_df = read_frame(facilities)
        fac_df = fac_df[[
            'PWSId',
            'FacName',
            'FacLong',
            'FacLat',
            'RegistryID',
        ]]
        fac_df.rename(columns={
            'FacLong': 'long',
            'FacLat': 'lat',
        }, inplace=True)
        systems_df = pd.merge(systems_df, fac_df, on='PWSId')
        # remove all systems that do not have a fips code
        systems_df['FIPSCodes'].dropna(inplace = True)
        # drop duplicate rows
        systems_df.drop_duplicates(subset = ['PWSId'], inplace = True)
        # this only takes the first listed value in FIPSCodes
        # can potentially change it to take all values and split into new rows
        systems_df['FIPSCodes'] = systems_df['FIPSCodes'].str.split(',', expand = True)[0]

        # in the event any of our violation scores are NaN, fill with 0
        systems_df['Viopaccr'].fillna(0, inplace = True)
        systems_df['Vioremain'].fillna(0, inplace = True)

        systems_df['facility_weighted_score'] = systems_df.apply(lambda x: self._calc_facility_score(x), axis = 1)
        systems_df['IsCommWaterSystem'] = systems_df['PWSTypeCode'] == 'CWS'

        # sum the populations and weighted scores
        fips_populations = systems_df.groupby(['FIPSCodes', 'IsCommWaterSystem'])['PopulationServedCount'].sum()
        fips_weighted_scores = systems_df.groupby(['FIPSCodes', 'IsCommWaterSystem'])['facility_weighted_score'].sum()
        
        # combine values into one dataframe
        comb_fips = pd.concat([fips_populations, fips_weighted_scores], axis = 1).reset_index()
        # evaluate adjusted score by dividing score by total population served
        comb_fips['score'] = comb_fips['facility_weighted_score'] / comb_fips['PopulationServedCount']

        comb_fips = comb_fips.groupby(['FIPSCodes'])['score'].sum().reset_index()
        comb_fips.drop_duplicates(inplace = True)
        # todo: figure out why this isn't working; some items come back as float instead of list
        comb_fips['systems'] = comb_fips.apply(lambda x: systems_df[systems_df['FIPSCodes'] == x['FIPSCodes']], axis = 1)
        return comb_fips

    def calc_state_scores(self, state, print_test = False):
        if print_test:
            log('state: %s' % (state), 'success')

        state_locs = app_models.location.objects.filter(state = state)
        state_df = read_frame(state_locs)
        area_scores = self._calc_area_score(state)
        if area_scores.shape[0] == 0 or state_df.shape[0] == 0:
            state_df['score'] = 0
            return state_df
        state_df["fips_county"] = state_df.apply(lambda x: str(x['fips_county']).rstrip('0').rstrip('.').zfill(5), axis = 1)
        area_scores["FIPSCodes"] = area_scores.apply(lambda x: str(x['FIPSCodes']).rstrip('0').rstrip('.').zfill(5), axis = 1)
        area_df = pd.merge(area_scores, state_df, left_on='FIPSCodes', right_on='fips_county', how='right')
        area_df['score'].fillna(0, inplace=True)
        return area_df
