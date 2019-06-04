from rawdata.models import EpaSystem
from app import models

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

    def _calc_current_score(self, voiremain):
        # voiremain current score
        if (voiremain >= self._CURRENT_MAX_SCORE ):
            return 1

        return voiremain / self._CURRENT_MAX_SCORE

    def _calc_facility_score(self, viopaccr , voiremain, pop_served):
        historical_score = self._calc_historical_score(viopaccr)
        current_score = self._calc_current_score(voiremain)

        return (historical_score * self._HISTORICAL_SCORE_WEIGHT) + (current_score * self._CURRENT_SCORE_WEIGHT) * pop_served

    def _pws_type_score(self, facilities):

        cws_score = 0
        cws_population = 0
        other_population = 0
        other_score = 0
        for facility in facilities:
            if (facility['pwstype'] == 'cws' ):
                cws_population += facility['population']
                cws_score += self._calc_facility_score(facility) * facility['population']
            else:
                other_population += facility['population']
                other_score += self._calc_facility_score(facility) * facility['population']

        cumulative_cws_score = (cws_score / cws_population) * self._COMMUNITY_WATER_SYSTEM_WEIGHT
        cumlative_other_score =  (other_score / other_population) * self._OTHER_WATER_SYSTEM_WEIGHT

        return ( cumulative_cws_score, cumlative_other_score )

    def _calc_area_score(self, areas):

        for area in areas:
            cws_score, other_score = _pws_type_score( area['facilities'])

        return cws_score + other_score

    def calc_all_scores(self):
        pass
