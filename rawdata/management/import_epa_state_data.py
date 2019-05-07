from rawdata.models import EpaSystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import json
import sys
import os
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        jsonDirectory = os.path.join(settings.BASE_DIR, settings.EPA_STATE_DATA_DIRECTORY)
        processed_rows = 0

        for filename in os.listdir(jsonDirectory):
            with open(os.path.join(jsonDirectory, filename)) as f:
                data = json.loads(f.read())

            for system in data["Results"]["WaterSystems"]:
                if system['PWSActivityCode'] != 'A':
                    continue # we only want active sites so skip others
                try:
                    processed_rows += 1 
                    self.add_system_to_db(system)
                    if (processed_rows % 10000 == 0):
                        self.stdout.write('Processed row %s...' %processed_rows)
                except utils.IntegrityError:
                    self.stdout.write('%s already in the db' % system["PWSId"])
                except:
                    self.stdout.write(system)
                    raise


    def add_system_to_db(self, system):
        # TODO use object.get_or_add? need to make sure this doesn't duplicate each time
        # just truncate the table and reimport? or maybe EpaSystem.objects.all().delete() if FK matters
        obj = EpaSystem(PWSName=system["PWSName"],
            PWSId=system["PWSId"],
            CitiesServed=system["CitiesServed"],
            StateCode=system["StateCode"],
            ZipCodesServed=system["ZipCodesServed"],
            CountiesServed=system["CountiesServed"],
            EPARegion=system["EPARegion"],
            PWSTypeCode=system["PWSTypeCode"],
            PrimarySourceCode=system["PrimarySourceCode"],
            PrimarySourceDesc=system["PrimarySourceDesc"],
            PopulationServedCount=system["PopulationServedCount"],
            PWSActivityCode=system["PWSActivityCode"],
            PWSActivityDesc=system["PWSActivityDesc"],
            OwnerTypeCode=system["OwnerTypeCode"],
            OwnerDesc=system["OwnerDesc"],
            QtrsWithVio=system["QtrsWithVio"],
            QtrsWithSNC=system["QtrsWithSNC"],
            SeriousViolator=system["SeriousViolator"],
            HealthFlag=system["HealthFlag"],
            MrFlag=system["MrFlag"],
            PnFlag=system["PnFlag"],
            OtherFlag=system["OtherFlag"],
            NewVioFlag=system["NewVioFlg"],
            RulesVio3yr=system["RulesVio3yr"],
            RulesVio=system["RulesVio"],
            Viopaccr=system["Viopaccr"],
            Vioremain=system["Vioremain"],
            Viofeanot=system["Viofeanot"],
            Viortcfea=system["Viortcfea"],
            Viortcnofea=system["Viortcnofea"],
            Ifea=system["Ifea"],
            Feas=system["Feas"],
            SDWDateLastIea=format_date(system["SDWDateLastIea"]),
            SDWDateLastIeaEPA=format_date(system["SDWDateLastIeaEPA"]),
            SDWDateLastIeaSt=format_date(system["SDWDateLastIeaSt"]),
            SDWDateLastFea=format_date(system["SDWDateLastFea"]),
            SDWDateLastFeaEPA=format_date(system["SDWDateLastFeaEPA"]),
            SDWDateLastFeaSt=format_date(system["SDWDateLastFeaSt"]),
            SDWAContaminantsInViol3yr=system["SDWAContaminantsInViol3yr"],
            SDWAContaminantsInCurViol=system["SDWAContaminantsInCurViol"],
            PbAle=system["PbAle"],
            CuAle=system["CuAle"],
            Rc350Viol=system["Rc350Viol"],
            DfrUrl=system["DfrUrl"],
            FIPSCodes=system["FIPSCodes"],
            SNC=system["SNC"],
            GwSwCode=system["GwSwCode"],
            SDWA3yrComplQtrsHistory=system["SDWA3yrComplQtrsHistory"],
            SDWAContaminants=system["SDWAContaminants"],
            PbViol=system["PbViol"],
            CuViol=system["CuViol"],
            LeadAndCopperViol=system["LeadAndCopperViol"],
            TribalFlag=system["TRIbalFlag"],  # yes, it's TRI
            FeaFlag=system["FeaFlag"],
            IeaFlag=system["IeaFlag"],
            SNCFlag=system["SNCFlag"],
            CurrVioFlag=system["CurrVioFlag"],
            VioFlag=system["VioFlag"],
            Insp5yrFlag=system["Insp5yrFlag"],
            Sansurvey5yr=system["Sansurvey5yr"],
            SignificantDeficiencyCount=system["SignificantDeficiencyCount"],
            SDWDateLastVisit=format_date(system["SDWDateLastVisit"]),
            SDWDateLastVisitEPA=format_date(system["SDWDateLastVisitEPA"]),
            SDWDateLastVisitState=format_date(system["SDWDateLastVisitState"]),
            SDWDateLastVisitLocal=format_date(system["SDWDateLastVisitLocal"]),
            SiteVisits5yrAll=system["SiteVisits5yrAll"],
            SiteVisits5yrInspections=system["SiteVisits5yrInspections"],
            SiteVisits5yrOther=system["SiteVisits5yrOther"],
            MaxScore=system["MaxScore"]
        )
        obj.save()


def format_date(date_string):
    '''convert the dd/mm/yyyy format into a datetime object'''
    if date_string:
        return datetime.strptime(date_string, '%m/%d/%Y')
    return None
