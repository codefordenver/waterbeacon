from rawdata.models import EpaFacilitySystem, EpaWaterSystem
from datetime import datetime
from django.db import utils
from decimal import Decimal


class SDW_Importer(object):

    def _format_date(self, date_string):
        '''convert the dd/mm/yyyy format into a datetime object'''
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y')
        return None


    def _format_int(self, int_string):
        '''deal with the annoying empty string to int exception'''
        if not int_string:
            return 0
        return int(int_string)


    def _format_decimal(self, decimal_string):
        '''deal with the annoying empty string exception'''
        if not decimal_string:
            return Decimal(0)
        return Decimal(decimal_string)


    def add_watersystem_to_db(self, system):
        # This doesn't need to support multithreaded running so not using update_or_create / get_or_create as ensuring it's changed/updated
        # seems very clunky. but it's possible that I'm just being foolish /shrug
        EpaWaterSystem.objects.update_or_create(PWSId=system["PWSId"],
        defaults = {'PWSName': system["PWSName"],
                'CitiesServed': system["CitiesServed"],
                'StateCode': system["StateCode"],
                'ZipCodesServed': system["ZipCodesServed"],
                'CountiesServed': system["CountiesServed"],
                'EPARegion': system["EPARegion"],
                'PWSTypeCode': system["PWSTypeCode"],
                'PrimarySourceCode': system["PrimarySourceCode"],
                'PrimarySourceDesc': system["PrimarySourceDesc"],
                'PopulationServedCount': self._format_int(system["PopulationServedCount"]),
                'PWSActivityCode': system["PWSActivityCode"],
                'PWSActivityDesc': system["PWSActivityDesc"],
                'OwnerTypeCode': system["OwnerTypeCode"],
                'OwnerDesc': system["OwnerDesc"],
                'QtrsWithVio': self._format_int(system["QtrsWithVio"]),
                'QtrsWithSNC': self._format_int(system["QtrsWithSNC"]),
                'SeriousViolator': system["SeriousViolator"],
                'HealthFlag': system["HealthFlag"],
                'MrFlag': system["MrFlag"],
                'PnFlag': system["PnFlag"],
                'OtherFlag': system["OtherFlag"],
                'NewVioFlag': system["NewVioFlg"],
                'RulesVio3yr': self._format_int(system["RulesVio3yr"]),
                'RulesVio': self._format_int(system["RulesVio"]),
                'Viopaccr': self._format_int(system["Viopaccr"]),
                'Vioremain': self._format_int(system["Vioremain"]),
                'Viofeanot': self._format_int(system["Viofeanot"]),
                'Viortcfea': self._format_int(system["Viortcfea"]),
                'Viortcnofea': self._format_int(system["Viortcnofea"]),
                'Ifea': system["Ifea"],
                'Feas': system["Feas"],
                'SDWDateLastIea': self._format_date(system["SDWDateLastIea"]),
                'SDWDateLastIeaEPA': self._format_date(system["SDWDateLastIeaEPA"]),
                'SDWDateLastIeaSt': self._format_date(system["SDWDateLastIeaSt"]),
                'SDWDateLastFea': self._format_date(system["SDWDateLastFea"]),
                'SDWDateLastFeaEPA': self._format_date(system["SDWDateLastFeaEPA"]),
                'SDWDateLastFeaSt': self._format_date(system["SDWDateLastFeaSt"]),
                'SDWAContaminantsInViol3yr': system["SDWAContaminantsInViol3yr"],
                'SDWAContaminantsInCurViol': system["SDWAContaminantsInCurViol"],
                'PbAle': system["PbAle"],
                'CuAle': system["CuAle"],
                'Rc350Viol': self._format_int(system["Rc350Viol"]),
                'DfrUrl': system["DfrUrl"],
                'FIPSCodes': system["FIPSCodes"],
                'SNC': system["SNC"],
                'GwSwCode': system["GwSwCode"],
                'SDWA3yrComplQtrsHistory': system["SDWA3yrComplQtrsHistory"],
                'SDWAContaminants': system["SDWAContaminants"],
                'PbViol': self._format_int(system["PbViol"]),
                'CuViol': self._format_int(system["CuViol"]),
                'LeadAndCopperViol': self._format_int(system["LeadAndCopperViol"]),
                'TribalFlag': system["TRIbalFlag"],  # yes, it's TRI
                'FeaFlag': system["FeaFlag"],
                'IeaFlag': system["IeaFlag"],
                'SNCFlag': system["SNCFlag"],
                'CurrVioFlag': self._format_int(system["CurrVioFlag"]),
                'VioFlag': self._format_int(system["VioFlag"]),
                'Insp5yrFlag': self._format_int(system["Insp5yrFlag"]),
                'Sansurvey5yr': self._format_int(system["Sansurvey5yr"]),
                'SignificantDeficiencyCount': self._format_int(system["SignificantDeficiencyCount"]),
                'SDWDateLastVisit': self._format_date(system["SDWDateLastVisit"]),
                'SDWDateLastVisitEPA': self._format_date(system["SDWDateLastVisitEPA"]),
                'SDWDateLastVisitState': self._format_date(system["SDWDateLastVisitState"]),
                'SDWDateLastVisitLocal': self._format_date(system["SDWDateLastVisitLocal"]),
                'SiteVisits5yrAll': self._format_int(system["SiteVisits5yrAll"]),
                'SiteVisits5yrInspections': self._format_int(system["SiteVisits5yrInspections"]),
                'SiteVisits5yrOther': self._format_int(system["SiteVisits5yrOther"]),
                'MaxScore': self._format_int(system["MaxScore"])
        })


    def add_epafacility_to_db(self, facility):
        EpaFacilitySystem.objects.update_or_create(RegistryID=facility["RegistryID"],
            defaults={'FacName': facility["FacName"],
                'PWSId': facility["SDWAIDs"],
                'FacStreet': facility["FacStreet"],
                'FacCity': facility["FacCity"],
                'FacState': facility["FacState"],
                'FacZip': facility["FacZip"],
                'FacCounty': facility["FacCounty"],
                'FacFIPSCode': facility["FacFIPSCode"],
                'FacDerivedZip': facility["FacDerivedZip"],
                'FacEPARegion': facility["FacEPARegion"],
                'FacLat': self._format_decimal(facility["FacLat"]),
                'FacLong': self._format_decimal(facility["FacLong"]),
                'FacAccuracyMeters': self._format_decimal(facility["FacAccuracyMeters"]),
                'FacReferencePoint': facility["FacReferencePoint"],
                'FacTotalPenalties': facility["FacTotalPenalties"],
                'FacDateLastPenalty': self._format_date(facility["FacDateLastPenalty"]),
                'FacLastPenaltyAmt': facility["FacLastPenaltyAmt"],
                'SDWAFormalActionCount': self._format_int(facility["SDWAFormalActionCount"]),
                'SDWASystemTypes': facility["SDWASystemTypes"],
                'FacDerivedStctyFIPS': facility["FacDerivedStctyFIPS"],
                'FacPercentMinority': self._format_decimal(facility["FacPercentMinority"]),
                'FacMajorFlag': facility["FacMajorFlag"],
                'ViolFlag': self._format_int(facility["ViolFlag"]),
                'CurrVioFlag': self._format_int(facility["CurrVioFlag"]),
                'FacPenaltyCount': self._format_int(facility["FacPenaltyCount"]),
                'FacFormalActionCount': self._format_int(facility["FacFormalActionCount"]),
                'SDWA3yrComplQtrsHistory': facility["SDWA3yrComplQtrsHistory"],
                'SDWAInspections5yr': self._format_int(facility["SDWAInspections5yr"]),
                'SDWAInformalCount': self._format_int(facility["SDWAInformalCount"]),
                'FacCollectionMethod': facility["FacCollectionMethod"],
                'FacStdCountyName': facility["FacStdCountyName"],
                'SDWISFlag': facility["SDWISFlag"],
                'FacImpWaterFlg': facility["FacImpWaterFlg"],
                'Score': facility["Score"] 
                      })
