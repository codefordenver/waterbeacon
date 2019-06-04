from rawdata.models import EpaWaterSystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import unicodecsv as csv
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import ( SDW_Importer )

class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        jsonDirectory = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'WaterSystems')
        processed_rows = 0

        importer = SDW_Importer()
        for filename in os.listdir(jsonDirectory):
            with open(os.path.join(jsonDirectory, filename)) as f:
                data = csv.reader(f)

                columns = []
                line_cnt = -1
                for system in data:
                    line_cnt += 1
                    if line_cnt == 0:
                        columns = system
                        continue
                    if system[columns.index('PWSActivityCode')] != 'A':
                        continue # we only want active sites so skip others
                    try:
                        processed_rows += 1
                        importer.add_watersystem_to_db(system, columns)
                        if (processed_rows % 10000 == 0):
                            self.stdout.write('Processed row %s...' %processed_rows)
                    except utils.IntegrityError:
                        self.stdout.write('%s already in the db' % system[columns.index("PWSId")])
                    except:
                        self.stdout.write('%s' %system)
                        raise


    def add_watersystem_to_db(self, system, columns):
        # This doesn't need to support multithreaded running so not using update_or_create / get_or_create as ensuring it's changed/updated
        # seems very clunky. but it's possible that I'm just being foolish /shrug
        EpaWaterSystem.objects.update_or_create(PWSId=system[columns.index("PWSId")],
        defaults = {'PWSName': system[columns.index("PWSName")],
                'CitiesServed': system[columns.index("CitiesServed")],
                'StateCode': system[columns.index("StateCode")],
                'ZipCodesServed': system[columns.index("ZipCodesServed")],
                'CountiesServed': system[columns.index("CountiesServed")],
                'EPARegion': system[columns.index("EPARegion")],
                'PWSTypeCode': system[columns.index("PWSTypeCode")],
                'PrimarySourceCode': system[columns.index("PrimarySourceCode")],
                'PrimarySourceDesc': system[columns.index("PrimarySourceDesc")],
                'PopulationServedCount': format_int(system[columns.index("PopulationServedCount")]),
                'PWSActivityCode': system[columns.index("PWSActivityCode")],
                'PWSActivityDesc': system[columns.index("PWSActivityDesc")],
                'OwnerTypeCode': system[columns.index("OwnerTypeCode")],
                'OwnerDesc': system[columns.index("OwnerDesc")],
                'QtrsWithVio': format_int(system[columns.index("QtrsWithVio")]),
                'QtrsWithSNC': format_int(system[columns.index("QtrsWithSNC")]),
                'SeriousViolator': system[columns.index("SeriousViolator")],
                'HealthFlag': system[columns.index("HealthFlag")],
                'MrFlag': system[columns.index("MrFlag")],
                'PnFlag': system[columns.index("PnFlag")],
                'OtherFlag': system[columns.index("OtherFlag")],
                'NewVioFlag': system[columns.index("NewVioFlg")],
                'RulesVio3yr': format_int(system[columns.index("RulesVio3yr")]),
                'RulesVio': format_int(system[columns.index("RulesVio")]),
                'Viopaccr': format_int(system[columns.index("Viopaccr")]),
                'Vioremain': format_int(system[columns.index("Vioremain")]),
                'Viofeanot': format_int(system[columns.index("Viofeanot")]),
                'Viortcfea': format_int(system[columns.index("Viortcfea")]),
                'Viortcnofea': format_int(system[columns.index("Viortcnofea")]),
                'Ifea': system[columns.index("Ifea")],
                'Feas': system[columns.index("Feas")],
                'SDWDateLastIea': format_date(system[columns.index("SDWDateLastIea")]),
                'SDWDateLastIeaEPA': format_date(system[columns.index("SDWDateLastIeaEPA")]),
                'SDWDateLastIeaSt': format_date(system[columns.index("SDWDateLastIeaSt")]),
                'SDWDateLastFea': format_date(system[columns.index("SDWDateLastFea")]),
                'SDWDateLastFeaEPA': format_date(system[columns.index("SDWDateLastFeaEPA")]),
                'SDWDateLastFeaSt': format_date(system[columns.index("SDWDateLastFeaSt")]),
                'SDWAContaminantsInViol3yr': system[columns.index("SDWAContaminantsInViol3yr")],
                'SDWAContaminantsInCurViol': system[columns.index("SDWAContaminantsInCurViol")],
                'PbAle': system[columns.index("PbAle")],
                'CuAle': system[columns.index("CuAle")],
                'Rc350Viol': format_int(system[columns.index("Rc350Viol")]),
                'DfrUrl': system[columns.index("DfrUrl")],
                'FIPSCodes': system[columns.index("FIPSCodes")],
                'SNC': system[columns.index("SNC")],
                'GwSwCode': system[columns.index("GwSwCode")],
                'SDWA3yrComplQtrsHistory': system[columns.index("SDWA3yrComplQtrsHistory")],
                'SDWAContaminants': system[columns.index("SDWAContaminants")],
                'PbViol': format_int(system[columns.index("PbViol")]),
                'CuViol': format_int(system[columns.index("CuViol")]),
                'LeadAndCopperViol': format_int(system[columns.index("LeadAndCopperViol")]),
                'TribalFlag': system[columns.index("TRIbalFlag")],  # yes, it's TRI
                'FeaFlag': system[columns.index("FeaFlag")],
                'IeaFlag': system[columns.index("IeaFlag")],
                'SNCFlag': system[columns.index("SNCFlag")],
                'CurrVioFlag': format_int(system[columns.index("CurrVioFlag")]),
                'VioFlag': format_int(system[columns.index("VioFlag")]),
                'Insp5yrFlag': format_int(system[columns.index("Insp5yrFlag")]),
                'Sansurvey5yr': format_int(system[columns.index("Sansurvey5yr")]),
                'SignificantDeficiencyCount': format_int(system[columns.index("SignificantDeficiencyCount")]),
                'SDWDateLastVisit': format_date(system[columns.index("SDWDateLastVisit")]),
                'SDWDateLastVisitEPA': format_date(system[columns.index("SDWDateLastVisitEPA")]),
                'SDWDateLastVisitState': format_date(system[columns.index("SDWDateLastVisitState")]),
                'SDWDateLastVisitLocal': format_date(system[columns.index("SDWDateLastVisitLocal")]),
                'SiteVisits5yrAll': format_int(system[columns.index("SiteVisits5yrAll")]),
                'SiteVisits5yrInspections': format_int(system[columns.index("SiteVisits5yrInspections")]),
                'SiteVisits5yrOther': format_int(system[columns.index("SiteVisits5yrOther")]),
                'MaxScore': format_int(system[columns.index("MaxScore")])
        })
 
            # obj = EpaWaterSystem(
            #     PWSName=system[columns.index("PWSName")],
            #     CitiesServed=system[columns.index("CitiesServed")],
            #     StateCode=system[columns.index("StateCode")],
            #     ZipCodesServed=system[columns.index("ZipCodesServed")],
            #     CountiesServed=system[columns.index("CountiesServed")],
            #     EPARegion=system[columns.index("EPARegion")],
            #     PWSTypeCode=system[columns.index("PWSTypeCode")],
            #     PrimarySourceCode=system[columns.index("PrimarySourceCode")],
            #     PrimarySourceDesc=system[columns.index("PrimarySourceDesc")],
            #     PopulationServedCount=format_int(system[columns.index("PopulationServedCount")]),
            #     PWSActivityCode=system[columns.index("PWSActivityCode")],
            #     PWSActivityDesc=system[columns.index("PWSActivityDesc")],
            #     OwnerTypeCode=system[columns.index("OwnerTypeCode")],
            #     OwnerDesc=system[columns.index("OwnerDesc")],
            #     QtrsWithVio=format_int(system[columns.index("QtrsWithVio")]),
            #     QtrsWithSNC=format_int(system[columns.index("QtrsWithSNC")]),
            #     SeriousViolator=system[columns.index("SeriousViolator")],
            #     HealthFlag=system[columns.index("HealthFlag")],
            #     MrFlag=system[columns.index("MrFlag")],
            #     PnFlag=system[columns.index("PnFlag")],
            #     OtherFlag=system[columns.index("OtherFlag")],
            #     NewVioFlag=system[columns.index("NewVioFlg")],
            #     RulesVio3yr=format_int(system[columns.index("RulesVio3yr")]),
            #     RulesVio=format_int(system[columns.index("RulesVio")]),
            #     Viopaccr=format_int(system[columns.index("Viopaccr")]),
            #     Vioremain=format_int(system[columns.index("Vioremain")]),
            #     Viofeanot=format_int(system[columns.index("Viofeanot")]),
            #     Viortcfea=format_int(system[columns.index("Viortcfea")]),
            #     Viortcnofea=format_int(system[columns.index("Viortcnofea")]),
            #     Ifea=system[columns.index("Ifea")],
            #     Feas=system[columns.index("Feas")],
            #     SDWDateLastIea=format_date(system[columns.index("SDWDateLastIea")]),
            #     SDWDateLastIeaEPA=format_date(system[columns.index("SDWDateLastIeaEPA")]),
            #     SDWDateLastIeaSt=format_date(system[columns.index("SDWDateLastIeaSt")]),
            #     SDWDateLastFea=format_date(system[columns.index("SDWDateLastFea")]),
            #     SDWDateLastFeaEPA=format_date(system[columns.index("SDWDateLastFeaEPA")]),
            #     SDWDateLastFeaSt=format_date(system[columns.index("SDWDateLastFeaSt")]),
            #     SDWAContaminantsInViol3yr=system[columns.index("SDWAContaminantsInViol3yr")],
            #     SDWAContaminantsInCurViol=system[columns.index("SDWAContaminantsInCurViol")],
            #     PbAle=system[columns.index("PbAle")],
            #     CuAle=system[columns.index("CuAle")],
            #     Rc350Viol=format_int(system[columns.index("Rc350Viol")]),
            #     DfrUrl=system[columns.index("DfrUrl")],
            #     FIPSCodes=system[columns.index("FIPSCodes")],
            #     SNC=system[columns.index("SNC")],
            #     GwSwCode=system[columns.index("GwSwCode")],
            #     SDWA3yrComplQtrsHistory=system[columns.index("SDWA3yrComplQtrsHistory")],
            #     SDWAContaminants=system[columns.index("SDWAContaminants")],
            #     PbViol=format_int(system[columns.index("PbViol")]),
            #     CuViol=format_int(system[columns.index("CuViol")]),
            #     LeadAndCopperViol=format_int(system[columns.index("LeadAndCopperViol")]),
            #     TribalFlag=system[columns.index("TRIbalFlag")],  # yes, it's TRI
            #     FeaFlag=system[columns.index("FeaFlag")],
            #     IeaFlag=system[columns.index("IeaFlag")],
            #     SNCFlag=system[columns.index("SNCFlag")],
            #     CurrVioFlag=format_int(system[columns.index("CurrVioFlag")]),
            #     VioFlag=format_int(system[columns.index("VioFlag")]),
            #     Insp5yrFlag=format_int(system[columns.index("Insp5yrFlag")]),
            #     Sansurvey5yr=format_int(system[columns.index("Sansurvey5yr")]),
            #     SignificantDeficiencyCount=format_int(system[columns.index("SignificantDeficiencyCount")]),
            #     SDWDateLastVisit=format_date(system[columns.index("SDWDateLastVisit")]),
            #     SDWDateLastVisitEPA=format_date(system[columns.index("SDWDateLastVisitEPA")]),
            #     SDWDateLastVisitState=format_date(system[columns.index("SDWDateLastVisitState")]),
            #     SDWDateLastVisitLocal=format_date(system[columns.index("SDWDateLastVisitLocal")]),
            #     SiteVisits5yrAll=format_int(system[columns.index("SiteVisits5yrAll")]),
            #     SiteVisits5yrInspections=format_int(system[columns.index("SiteVisits5yrInspections")]),
            #     SiteVisits5yrOther=format_int(system[columns.index("SiteVisits5yrOther")]),
            #     MaxScore=format_int(system[columns.index("MaxScore")])
            #)
            #obj.save()
        

def format_date(date_string):
    '''convert the dd/mm/yyyy format into a datetime object'''
    if date_string:
        return datetime.strptime(date_string, '%m/%d/%Y')
    return None


def format_int(int_string):
    '''deal with the annoying emptry string to int exception'''
    if not int_string:
        return 0
    return int(int_string)
