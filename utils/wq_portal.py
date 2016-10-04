import requests
import pandas as pd

clas wq_portal(object):
	host = 'www.waterqualitydata.us'
	
	sorted = 'no'
	sampleMedia = 'Water'
	characteristicType = ''
	characteristicName = ''

	def __init__(self, mimeType = 'csv'):
		self.mimeType = mimeType = 'csv'
		self.df = None

	def getData(self, statecode = None, 
				countycode = None, 
				siteType = None, 
				organization = None
				siteid = None,
				startDate = None
				):
		pass
	
	def to_csv(self):
		pass
	
	def to_xlsx(self):
		pass

	def df(self):
		return self.df

	def cli(self):
		pass

if __name__ == '__main__':
	pass