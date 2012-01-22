def populate_professionals_without_geocodes():
	from geopy import geocoders
	from rolodx.main.models import Professional
	import sys, traceback
	import decimal
	pros = Professional.objects.filter(address_latitude=None)
	g = geocoders.Google(domain='maps.google.ca')
	for pro in pros:
		if pro.street_address != None:
			try:
				addr, (lat, lng) = g.geocode(pro.street_address)
			except:
				traceback.print_exc(file=sys.stdout)
				continue
			pro.address_latitude = decimal.Decimal(repr(lat))
			pro.address_longitude = decimal.Decimal(repr(lng))
			print lat,lng
			pro.save()
