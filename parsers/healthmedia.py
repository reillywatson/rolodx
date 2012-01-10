import re
from parsecommon import PageRetriever

getPage = PageRetriever('http://www.ontariodoctordirectory.ca').getPage

def tryMatch(pattern, text):
	result = ''
	match = re.search(pattern, text)
	if match != None:
		result = match.group(1).strip()
	return result

def addDoc(url, city):
	soup = getPage(url)
	docName = soup.findAll('strong')[1].text
	# take out the "view on map" junk
	soup.address.div.extract()
	address = soup.address
	addressComponents = [a for a in address.contents if 'text' not in dir(a)][1:]
	phone = tryMatch('Phone:(.*?)\n', soup.prettify())
	fax = tryMatch('Fax:(.*?)\n', soup.prettify())
	# TODO: how are we going to store addresses?
	print docName, addressComponents, phone, fax
	

def getcitylist():
	soup = getPage('http://www.ontariodoctordirectory.ca/')
	cities = [x.a for x in soup.find(id='footer').findAll('li')]
	for city in cities:
		cityname = city.text
		cityurl = city['href']
		docsInCity = parsecity(cityurl)
		for doc in docsInCity:
			addDoc(doc, cityname)

def parsecity(url):
	print 'link: ' + url
	cityUrlPortion = '/'.join(url.split('/')[:2])
	soup = getPage(url)
	docs = soup.findAll(href=re.compile('^'+cityUrlPortion+'/Doctor'))
	nextPage = soup.find(href=re.compile('^'+cityUrlPortion+'/\\d\\d?'))
	if nextPage != None:
		docs.extend(parsecity(nextPage['href']))
	print 'got %d doctors' % len(docs)
	return docs
