import pygeoip

# do I need to do something different to reference this on the server?
GEOIP_DATABASE = pygeoip.GeoIP('main/static/data/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
def lookup(ip):
	if ip == '127.0.0.1':
		ip = '66.203.195.152' # put in whatever test IP you want here
	record = GEOIP_DATABASE.record_by_addr(ip)
	print record
	if record != None:
		return (record['latitude'], record['longitude'])
	return None

