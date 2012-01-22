def geocode(address):
	import requests
	import json
	import urllib
	r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % urllib.quote(address))
	response = json.loads(r.content)
	results = response['results']
	if len(results) == 0:
		print 'no results for address %s' % address
		return None
	coords = response['results'][0]['geometry']['location']
	# updating the models with these might be a good idea
	# sweetaddress = response['results'][0]['formatted_address']
	return (coords['lat'],coords['lng'])

def populate_professionals_without_geocodes():
	from rolodx.main.models import Professional
	import decimal
	pros = Professional.objects.filter(address_latitude=None)
	for pro in pros:
		if pro.street_address != None:
			code = geocode(pro.street_address)
			if code != None:
				pro.address_latitude = decimal.Decimal(repr(code[0]))
				pro.address_longitude = decimal.Decimal(repr(code[1]))
				print code
				pro.save()
