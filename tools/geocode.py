def populate_professionals_without_geocodes():
	from geopy import geocoders
	from rolodx.main.models import Professional
	import sys, traceback
	import decimal
	pros = Professional.objects.filter(address_latitude=None)[100:]
	g = geocoders.Google()
	for pro in pros:
		if pro.street_address != None:
			try:
				results = g.geocode(pro.street_address, exactly_one=False)
			except:
				traceback.print_exc(file=sys.stdout)
				print 'failure address: %s' % pro.street_address
				continue
			pro.address_latitude = decimal.Decimal(repr(results[0][1][0]))
			pro.address_longitude = decimal.Decimal(repr(results[0][1][1]))
			print pro.street_address
			print pro.address_latitude, pro.address_longitude
			pro.save()
