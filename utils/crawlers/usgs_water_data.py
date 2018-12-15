from datetime import datetime, timedelta
import pandas as pd
from furl import furl

class usgs_water_data(object):
    # crawls for usgs nwis data

    def __init__(self):
        self.host = "waterdata.usgs.gov"
        self.format = "rdb"

    def get(self, site_num, end_date = datetime.today().strftime('%Y-%-m-%-d'), begin_date = (datetime.today() - timedelta(days = 7)).strftime('%Y-%-m-%-d') ):

        params = {
            'cb_00010':'on',
            'cb_00095':'on',
            'cb_00300':'on',
            'cb_00400':'on',
            'format': self.format,
            'site_no': site_num,
            'begin_date': begin_date,
            'end_date': end_date
        }

        # building url
        f = furl().set(scheme='https', host=self.host, path='/nwis/uv',args=params)

        # parse data
        df = pd.read_csv(f.url,sep='\t', header = 29)

        # drop unused columns
        df = df[1:]
        columns = ['agency_cd','site_no','210922_00010_cd','210923_00095_cd','210924_00300_cd','210925_00400_cd']
        df.drop(columns, inplace=True, axis=1)

        # rename columns
        df = df.rename(index=str, columns={"210922_00010": "temperature_celcius", "210923_00095": "conductance","210924_00300":"dissolved_oxygen","210925_00400":"ph"})

        # convert datetime string to pandas datetime
        df['datetime'] = df['datetime'].astype('datetime64[ns]')

        # convert column string type to float
        df['temperature_celcius'] = df['temperature_celcius'].astype(float)
        df['conductance'] = df['conductance'].astype(float)
        df['dissolved_oxygen'] = df['dissolved_oxygen'].astype(float)
        df['ph'] = df['ph'].astype(float)


        # set datetime object as index
        df = df.set_index('datetime')

        # resample data to days
        df = df.resample('D').mean()

        return df

if __name__ == "__main__":
    usgs = usgs_water_data()
    df = usgs.get('06711565')
