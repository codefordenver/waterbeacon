import requests
from lxml import html
from datetime import datetime

class remote_water_quality_monitoring_network(object):
	url = 'http://mdw.srbc.net/remotewaterquality/data_viewer.aspx'

	def __init__(self):
		pass

	def get(self):
		r1 = requests.get(self.url)
		if r1.status_code != 200:
			return []

		parsed1 = html.fromstring(r1.text)
		viewstate = parsed1.xpath('//input[@name="__VIEWSTATE"]/@value')[0]
		eventvalidation = parsed1.xpath('//input[@name="__EVENTVALIDATION"]/@value')[0]
		now = datetime.now()
		data = {

		'__VIEWSTATE':viewstate,
		'__EVENTVALIDATION':eventvalidation,
		'__VIEWSTATEENCRYPTED':'',
		'__EVENTTARGET':'',
		'__EVENTARGUMENT':'',
		'__LASTFOCUS':'',
		'txtStartDate':now.strftime('%-m/%-d/%Y'),
		'txtEndDate':now.strftime('%-m/%-d/%Y'),
		'ctrlRawData1$txtStartDate':now.strftime('%-m/%-d/%Y'),
		'ctrlRawData1$txtEndDate':now.strftime('%-m/%-d/%Y'),
		'ctrlStatistics1$txtStartDate':now.strftime('%-m/%-d/%Y'),
		'ctrlStatistics1$txtEndDate':now.strftime('%-m/%-d/%Y'),
		}
		r2 = requests.post(self.url, data=data, cookies=r1.cookies)
		parsed2 = html.fromstring(r2.text)
		out = []
		for row in parsed2.xpath('//tr[@class="divGridviewMostRecentRow"] | //tr[@class="divGridviewMostRecentAlternateRow"]'):
			out.append({
			 'station':row.xpath('td/span[contains(@id,"lblDescription")]/text()')[0].strip(),
			 'time':row.xpath('td/span[contains(@id,"lblSampleTime")]/text()')[1].replace('(','').replace(')','').strip(),
			 'temperature':row.xpath('td[@align="right"]/text()')[0].strip(),
			 'conductivity':row.xpath('td[@align="right"]/text()')[1].strip(),
			 'ph':row.xpath('td[@align="right"]/text()')[2].strip(),
			 'turbidity':row.xpath('td[@align="right"]/text()')[3].strip(),
			 'odo':row.xpath('td[@align="right"]/text()')[4].strip(),
			})
		return out

if __name__ == "__main__":
	crawler = remote_water_quality_monitoring_network()
	data = crawler.get()
