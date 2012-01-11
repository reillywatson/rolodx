import pickle
import re
import sys
import traceback
from parsecommon import PageRetriever

getPage = PageRetriever('http://www.yellowpages.ca').getPage

def parseBusiness(url):
	try:
		soup = getPage(url)
		businessName = soup.find('span', 'fn').text
		businessAddress = None
		addrParent = soup.find(id='busCardLeft')
		if addrParent and addrParent.p:
			businessAddress = addrParent.p.text
		businessCoordinates = None
		coordinates = soup.find('div', 'mapDivStyle')
		if coordinates != None:
			businessCoordinates = re.search('/Map/Road/(.*?)/', coordinates['style']).group(1).split(',')
		#http://dev.virtualearth.net/REST/v1/Imagery/Map/Road/43.806137,-79.545932
		businessPhoneNumber = None
		if soup.find('span', 'busPhoneNumber') != None:
			businessPhoneNumber = soup.find('span', 'busPhoneNumber').text
		businessUrl = None
		urlContainer = soup.find('div', 'busCardLeftLinks')
		if urlContainer != None and urlContainer.a != None:
			businessUrl = urlContainer.a['href'].replace('/gourl/', '')
		parentCatBreadcrumbs = soup.find('ul', 'ypgBreadcrumb')
		categories = None
		if parentCatBreadcrumbs != None and parentCatBreadcrumbs.findAll('a') != None:
			categories = [cat.text for cat in parentCatBreadcrumbs.findAll('a')[1:-1]]
		ypid = url.split('/')[-1].split('.')[0]
		businessInfo = {'name':businessName, 'address':businessAddress, 'coordinates':businessCoordinates, 'phone':businessPhoneNumber, 'ypid':ypid, 'website':businessUrl, 'category':categories}
		return businessInfo
	except:
		print 'failure! ' + url
		traceback.print_exc(file=sys.stdout)
		return None

def parseBusinessList(url):
	soup = getPage(url)
	businesses = []
	for bus in soup.findAll('h3', 'listingTitleLine'):
		businesses.append(parseBusiness(bus.a['href']))
	nextPage = soup.find('span', 'pagingNext')
	if nextPage != None and nextPage.a != None:
		businesses.extend(parseBusinessList(nextPage.a['href']))
	return businesses

def parseCategory(url):
	soup = getPage(url)
	categories = soup.findAll('div', 'ypgCategory')
	businesses = []
	for cat in categories:
		linkUrl = cat.a['href']
		if linkUrl.startswith('/search'):
			businesses.extend(parseBusinessList(linkUrl))
		else:
			businesses.extend(parseCategory(linkUrl))
	return businesses

def scrapeParrySound():
	businesses = parseCategory('http://www.yellowpages.ca/locations/Ontario/Parry+Sound')
	pickle.dump(businesses, 'parrysound.pickle')
	return businesses
