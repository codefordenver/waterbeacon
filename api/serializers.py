from app import models
from utils.log import log

def NodeSerializer(objs, request = None):
	data = {'results':{'nodes':[]},'meta':{'number_of_nodes':0}}

	for obj in objs:
		node = {
			'name':node.devicealias,
			'data':[],
			'source':node.sourcetype,
			'long':node.long,
			'lat':node.lat,
			'tags':[tag.name for tag in models.tag.objects.filter( node = obj) ]
		}

		for d in models.data.objects.filter(node = node):
			data = {
				'timstamp': d.timestamp,
				'sensor':d.source,
				'measurement':d.data,

			}
			node['data'].append(data)

		data['results']['nodes'].append(node)

	return data

def NewsSerializer(objs, request = None):
	data = {'results':{'nodes':[]},'meta':{'number_of_articles':0}}

	return data
