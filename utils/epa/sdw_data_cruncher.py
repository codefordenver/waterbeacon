from app import models as app_models
from rawdata import models as rawdata_models
from app import models as app_models
from utils.log import log

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

        return (historical_score * self._HISTORICAL_SCORE_WEIGHT) + (current_score * self._CURRENT_SCORE_WEIGHT)

    def _pws_type_score(self, systems):
        # for every facility there is one system
        cws_score = 0
        cws_population = 0
        other_population = 0
        other_score = 0

        # set all facilities in violations as false
        pwsids = systems.values_list("PWSId", flat=True).distinct()
        rawdata_models.EpaFacilitySystem.objects.filter( PWSId__in= pwsids).update(in_violation = False)

        for system in systems:
            if (system.PWSTypeCode == 'cws' ):
                cws_population += system.PopulationServedCount
                facility_score = self._calc_facility_score(system.Viopaccr, system.Vioremain, system.PopulationServedCount) * system.PopulationServedCount
                cws_score += facility_score
            else:
                other_population += system.PopulationServedCount
                facility_score = self._calc_facility_score(system.Viopaccr, system.Vioremain, system.PopulationServedCount) * system.PopulationServedCount
                other_score += facility_score

            if facility_score:
                rawdata_models.EpaFacilitySystem.objects.filter( PWSId = system.PWSId ).update(in_violation = True )

        if cws_population:
            cumulative_cws_score = (cws_score / cws_population) * self._COMMUNITY_WATER_SYSTEM_WEIGHT
        else:
            cumulative_cws_score = 0

        if other_population:
            cumlative_other_score =  (other_score / other_population) * self._OTHER_WATER_SYSTEM_WEIGHT
        else:
            cumlative_other_score = 0

        return ( cumulative_cws_score, cumlative_other_score )

    def _calc_area_score(self, county_fips):
        # single area represent a zipcode
        areas = []

        systems = rawdata_models.EpaWaterSystem.objects.filter( FIPSCodes__contains = county_fips )
        cws_score, other_score = self._pws_type_score(systems)

        return cws_score + other_score

    def calc_state_scores(self, state, print_test = False):
        areas = []

        if print_test:
            log('state: %s' % (state), 'success')

        for location in app_models.location.objects.filter( state = state).exclude(fips_county = ''):
            score = self._calc_area_score(location.fips_county)
            areas.append({
                'county_fips': location.fips_county,
                'score': score
            })

            if print_test:
                log('%s: %s' % (location.fips_county, round(score, 3)), 'success')

        return areas
