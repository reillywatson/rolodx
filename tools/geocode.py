def geocode(address):
	import requests
	import json
	import urllib
	response = json.loads(requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % urllib.quote(address)).content)
	coords = response['results'][0]['geometry']['location']
	# updating the models with these might be a good idea
	sweetaddress = response['results'][0]['formatted_address']
	return (coords['lat'],coords['lng'])
