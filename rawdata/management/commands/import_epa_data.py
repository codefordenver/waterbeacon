# from rawdata.models import EpaFacilitySystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import csv
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import (SDW_Importer)


class Command(BaseCommand):

    def get_facility_df(self, facility_df):
        cols_of_interest = ['FacDerivedStctyFIPS', 'FacState', 'Score', 'FacFIPSCode', 'FacName', 'FacZip', 'FacEPARegion', 'FacMajorFlag', 'NC', 'ViolFlag', 'FacCity', 'SDWAIDs', 'FacLat',
                            'FacCollectionMethod', 'CurrVioFlag', 'FacStdCountyName', 'SDWAInformalCount', 'FacDerivedZip', 'RegistryID', 'FacStreet', 'FacAccuracyMeters', 'FacCounty', 'FacLong']
        facility_df = facility_df[cols_of_interest]
        facility_df = facility_df.replace('\n', '', regex=True)
        facility_df["Score"] = facility_df["Score"].fillna(0)
        facility_df["FacDerivedStctyFIPS"] = facility_df["FacDerivedStctyFIPS"].fillna(
            0)
        facility_df["FacDerivedStctyFIPS"] = facility_df.apply(lambda x: str(
            x['FacDerivedStctyFIPS']).rstrip('0').rstrip('.').zfill(5), axis=1)
        facility_df["FacDerivedZip"] = facility_df["FacDerivedZip"].fillna(
            0)
        facility_df["FacDerivedZip"] = facility_df.apply(lambda x: str(
            x['FacDerivedZip']).rstrip('0').rstrip('.').zfill(5), axis=1)
        facility_df["FacEPARegion"] = facility_df["FacEPARegion"].fillna(
            0)
        facility_df["FacEPARegion"] = facility_df.apply(lambda x: str(
            x['FacEPARegion']).rstrip('0').rstrip('.').zfill(2), axis=1)
        facility_df.fillna('', inplace=True)

        return facility_df

    def get_watersystem_df(self, water_df):
        cols_of_interest = ['EPARegion', 'SNC', 'SDWDateLastFeaEPA', 'SDWDateLastFea', 'SignificantDeficiencyCount', 'DfrUrl', 'PrimarySourceDesc', 'SDWAContaminants', 'PWSTypeCode', 'CountiesServed', 'StateCode', 'ZipCodesServed', 'FIPSCodes', 'Viopaccr', 'Vioremain', 'MaxScore', 'VioFlag',
                            'RulesVio', 'PWSTypeDesc', 'Viortcfea', 'CitiesServed', 'PbViol', 'Viofeanot', 'PopulationServedCount', 'OwnerTypeCode', 'PWSId', 'PWSActivityDesc', 'HealthFlag', 'PWSName', 'SeriousViolator', 'PWSActivityCode', 'CurrVioFlag', 'Viortcnofea', 'CuViol', 'OtherFlag', 'NewVioFlg', 'RegistryID']
        water_df = water_df[cols_of_interest]

        return water_df

    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class FACILITY_TYPE = 'Facilities'
        watersystem_dir = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'WaterSystems')
        facility_dir = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'Facilities')
        facility_csv_files = os.listdir(facility_dir)
        watersystem_csv_files = os.listdir(watersystem_dir)
        processed_rows = 0

        importer = SDW_Importer()
        water_dtype = {
            'FIPSCodes': 'str',
            'RegistryID': 'str',
            'SDWDateLastVisitEPA': 'str'
        }
        fac_dtype = {
            'FacDerivedStctyFIPS': 'str',
            'FacFIPSCode': 'str',
            'RegistryID': 'str',
            'FacZip': 'str',
            'SDWDateLastVisitEPA': 'str'
        }

        # the file names match so we're just iterating and trying to see if we have the same name in either dir
        for watersystem_file_name in watersystem_csv_files:
            water_path = os.path.join(watersystem_dir, watersystem_file_name)
            facility_path = os.path.join(facility_dir, watersystem_file_name)
            try:
                water_df = pd.read_csv(water_path, dtype=water_dtype)
                if len(water_df) == 0:
                    self.stdout.write('skipping. no data in %s' % water_path)
                    continue
                water_df = self.get_watersystem_df(water_df)
            except:
                self.stdout.write('%s data corrupted' % water_path)
                continue
            if water_df.empty:
                continue
            try:
                facility_df = pd.read_csv(facility_path, dtype=fac_dtype)
                if len(facility_df) == 0:
                    self.stdout.write(
                        'skipping. no data in %s' % facility_path)
                    continue
                facility_df = self.get_facility_df(facility_df)

            except FileNotFoundError:
                self.stdout.write(
                    '%s no corresponding facility file. panic so let\'s skip' % facility_path)
                continue

            # remove all inactive sites

            # water_df=water_df[water_df['PWSActivityCode'] == 'A']
            final_df = pd.merge(water_df, facility_df,
                                how='outer', left_on='PWSId', right_on='SDWAIDs')
            final_df.fillna('', inplace=True)
            final_df['EPARegion'] = str(water_df['EPARegion'][0]).rstrip(
                '0').rstrip('.').zfill(2)

            for row in final_df.itertuples():
                processed_rows += 1
                if row.PWSActivityCode != 'A':  # only add active rows
                    continue
                importer.add_to_db(row)
                if (processed_rows % 10000 == 0):
                    self.stdout.write('Processed row %s...' % processed_rows)

        print('%s' % processed_rows)
