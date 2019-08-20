from pprint import PrettyPrinter
from rest_framework.test import (APITestCase, APIClient)

# ./manage.py test api.v1.tests.WaterBeaconTestCase --keepdb --settings=settings.dev
class WaterBeaconTestCase(APITestCase):
    # REF: https://waterbeacon.docs.apiary.io/#reference/0/data/submit-data
    fixtures = [
        './app/fixtures/test_data.json',
        './news/fixtures/locations.json',
        './news/fixtures/test_data.json',
    ]

    def setUp(self):
        self.pp = PrettyPrinter(indent=4)
        self.print_results = True

    def print_response(self, response, title):
        # prety print json output
        if self.print_results:
            self.pp.pprint(response.data)

    def test_get_locations(self):
        # ./manage.py test api.v1.tests.WaterBeaconTestCase.test_get_locations --keepdb --settings=settings.dev
        client = APIClient()
        params = {'sources': 'locations,news,utilities',
                'violation': 'true' }
        response = client.get('/v1/data/', data = params)
        self.assertEqual(response.status_code, 200)

        self.print_response(response, "test_get_locations")

        self.assertEqual(response.data['meta']['locations'], 86)
        self.assertEqual(response.data['meta']['cities'], 104)
        self.assertEqual(response.data['meta']['utilities'], 2918)
