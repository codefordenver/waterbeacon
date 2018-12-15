#use this url to understand Web Service https://www.waterqualitydata.us/webservices_documentation/

import pywqp_client

# use https://www.waterqualitydata.us/portal/
# Characteristics field to figure out characteristicNames

siteType = [

]

characteristicNames = [
    'Dissolved oxygen',
    'pH',
    'Temperature difference',
    'Nitrate',
    'Turbidity',
    'Total solids',
    'Phosphate',
    'BOD, ultimate' # biochemical oxygen demand
]

params = {'countrycode': 'US',
          'statecode': 'US:19',
          'countycode': 'US:19:015',
          'characteristicName': ';'.join(characteristicNames) }

# instantiating instance of pywqp_client class
client_instance = pywqp_client.RESTClient()

# request data from wqp database
response = client_instance.request_wqp_data(verb, host_url, resource_label, params, mime_type='text/csv')

# save to pandas dataframe
df = client_instance.response_as_pandas_dataframe(response)

# write to file
#client_instance.stash_response(response, 'temp/wqp.csv')

# retrieve url
#client_instance.create_rest_url(host_url, resource_label, params, mime_type='text/csv')
