from rawdata.models import EpaSystem
from datetime import datetime

class SDW_Importer(object):

    def _format_date(self, date_string):
        '''convert the dd/mm/yyyy format into a datetime object'''
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y')
        return None

    def _format_int(self, int_string):
        '''deal with the annoying emptry string to int exception'''
        if not int_string:
            return 0
        return int(int_string)

    def add_watersystem_to_db(self, system, columns):
        # TODO use object.get_or_add? need to make sure this doesn't duplicate each time
        # just truncate the table and reimport? or maybe EpaSystem.objects.all().delete() if FK matters
        obj = EpaSystem(
            PWSName=system[columns.index("PWSName")],
            PWSId=system[columns.index("PWSId")],
            CitiesServed=system[columns.index("CitiesServed")],
            StateCode=system[columns.index("StateCode")],
            ZipCodesServed=system[columns.index("ZipCodesServed")],
            CountiesServed=system[columns.index("CountiesServed")],
            EPARegion=system[columns.index("EPARegion")],
            PWSTypeCode=system[columns.index("PWSTypeCode")],
            PrimarySourceCode=system[columns.index("PrimarySourceCode")],
            PrimarySourceDesc=system[columns.index("PrimarySourceDesc")],
            PopulationServedCount=self._format_int(system[columns.index("PopulationServedCount")]),
            PWSActivityCode=system[columns.index("PWSActivityCode")],
            PWSActivityDesc=system[columns.index("PWSActivityDesc")],
            OwnerTypeCode=system[columns.index("OwnerTypeCode")],
            OwnerDesc=system[columns.index("OwnerDesc")],
            QtrsWithVio=self._format_int(system[columns.index("QtrsWithVio")]),
            QtrsWithSNC=self._format_int(system[columns.index("QtrsWithSNC")]),
            SeriousViolator=system[columns.index("SeriousViolator")],
            HealthFlag=system[columns.index("HealthFlag")],
            MrFlag=system[columns.index("MrFlag")],
            PnFlag=system[columns.index("PnFlag")],
            OtherFlag=system[columns.index("OtherFlag")],
            NewVioFlag=system[columns.index("NewVioFlg")],
            RulesVio3yr=self._format_int(system[columns.index("RulesVio3yr")]),
            RulesVio=self._format_int(system[columns.index("RulesVio")]),
            Viopaccr=self._format_int(system[columns.index("Viopaccr")]),
            Vioremain=self._format_int(system[columns.index("Vioremain")]),
            Viofeanot=self._format_int(system[columns.index("Viofeanot")]),
            Viortcfea=self._format_int(system[columns.index("Viortcfea")]),
            Viortcnofea=self._format_int(system[columns.index("Viortcnofea")]),
            Ifea=system[columns.index("Ifea")],
            Feas=system[columns.index("Feas")],
            SDWDateLastIea=self._format_date(system[columns.index("SDWDateLastIea")]),
            SDWDateLastIeaEPA=self._format_date(system[columns.index("SDWDateLastIeaEPA")]),
            SDWDateLastIeaSt=self._format_date(system[columns.index("SDWDateLastIeaSt")]),
            SDWDateLastFea=self._format_date(system[columns.index("SDWDateLastFea")]),
            SDWDateLastFeaEPA=self._format_date(system[columns.index("SDWDateLastFeaEPA")]),
            SDWDateLastFeaSt=self._format_date(system[columns.index("SDWDateLastFeaSt")]),
            SDWAContaminantsInViol3yr=system[columns.index("SDWAContaminantsInViol3yr")],
            SDWAContaminantsInCurViol=system[columns.index("SDWAContaminantsInCurViol")],
            PbAle=system[columns.index("PbAle")],
            CuAle=system[columns.index("CuAle")],
            Rc350Viol=self._format_int(system[columns.index("Rc350Viol")]),
            DfrUrl=system[columns.index("DfrUrl")],
            FIPSCodes=system[columns.index("FIPSCodes")],
            SNC=system[columns.index("SNC")],
            GwSwCode=system[columns.index("GwSwCode")],
            SDWA3yrComplQtrsHistory=system[columns.index("SDWA3yrComplQtrsHistory")],
            SDWAContaminants=system[columns.index("SDWAContaminants")],
            PbViol=self._format_int(system[columns.index("PbViol")]),
            CuViol=self._format_int(system[columns.index("CuViol")]),
            LeadAndCopperViol=self._format_int(system[columns.index("LeadAndCopperViol")]),
            TribalFlag=system[columns.index("TRIbalFlag")],  # yes, it's TRI
            FeaFlag=system[columns.index("FeaFlag")],
            IeaFlag=system[columns.index("IeaFlag")],
            SNCFlag=system[columns.index("SNCFlag")],
            CurrVioFlag=self._format_int(system[columns.index("CurrVioFlag")]),
            VioFlag=self._format_int(system[columns.index("VioFlag")]),
            Insp5yrFlag=self._format_int(system[columns.index("Insp5yrFlag")]),
            Sansurvey5yr=self._format_int(system[columns.index("Sansurvey5yr")]),
            SignificantDeficiencyCount=self._format_int(system[columns.index("SignificantDeficiencyCount")]),
            SDWDateLastVisit=self._format_date(system[columns.index("SDWDateLastVisit")]),
            SDWDateLastVisitEPA=self._format_date(system[columns.index("SDWDateLastVisitEPA")]),
            SDWDateLastVisitState=self._format_date(system[columns.index("SDWDateLastVisitState")]),
            SDWDateLastVisitLocal=self._format_date(system[columns.index("SDWDateLastVisitLocal")]),
            SiteVisits5yrAll=self._format_int(system[columns.index("SiteVisits5yrAll")]),
            SiteVisits5yrInspections=self._format_int(system[columns.index("SiteVisits5yrInspections")]),
            SiteVisits5yrOther=self._format_int(system[columns.index("SiteVisits5yrOther")]),
            MaxScore=self._format_int(system[columns.index("MaxScore")])
        )

        obj.save()
