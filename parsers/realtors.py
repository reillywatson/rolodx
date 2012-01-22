import pageretriever

# returns 151671 most-common surnames in the US, data is from
# http://www.census.gov/genealogy/www/data/2000surnames/index.html
def getsurnames():
	names = []
	for line in open('/home/reilly/Downloads/names/app_c.csv'):
		names.append(line.split(',')[0].lower())
	names = names[1:]
	return names

getPage = pageretriever.PageRetriever('http://www.realtor.ca/').getPageSoup

def parseRealtor(url):
	soup = getPage(url)

def getDetails(url):
	soup = getPage(url)
	if soup == None:
		return set()
	links = soup.findAll('a')
	urls = [a['href'] for a in links]
	details = [a for a in urls if 'RealtorDetails' in a]
	nextPage = [a for a in links if a.text == 'Next']
	if len(nextPage) > 0:
		details.extend(getDetails(nextPage[0]['href']))
	return set(details)

def searchsite():
	# let's just use the 1000 most common for now
	names = getsurnames()[1000:20000]
	details = set()
	for name in names:
		details = details.union(getDetails('http://www.realtor.ca/REALTORResults.aspx?&lastname=%s&ps=50'%name))
	return details


def tryMatch(pattern, text):
	import re
	result = ''
	match = re.search(pattern, text)
	if match != None:
		result = match.group(1).strip()
	return result

out = open('realtors.json', 'w')

def parserealtor(url):
	import titlecase, urllib, json
	soup = getPage(url)
	try:
		name = titlecase.titlecase(soup.find(id='_ctl0_elRealtorDetails_lblName').text)
		company = titlecase.titlecase(soup.find(id='_ctl0_elRealtorDetails_lblOrganization').text)
		phone = tryMatch('Telephone:(.*?)\n', soup.prettify())
		fax = tryMatch('Fax:(.*?)\n', soup.prettify())
		address = '\n'.join([a for a in soup.find(id='_ctl0_elRealtorDetails_lblOrganizationAddress').contents if 'text' not in dir(a)])
		address = company + '\n' + address
		website = ''
		websiteParent = soup.find(id='_ctl0_elRealtorDetails_lblRealtorWebsite')
		if websiteParent != None and websiteParent.a != None:
			website = urllib.unquote(websiteParent.a['href'].split('=')[-1])
		categories = []
		specialtyParent = soup.find(id='_ctl0_elRealtorDetails_pnlSpecialties')
		if specialtyParent != None:
			categories = [a.text for a in specialtyParent.findAll('td')]
		data = {'name':name, 'address':address,'fax':fax,'phone':phone, 'categories':categories, 'website':website}
		out.write(json.dumps(data))
	except:
		pass

def parseurllist():
	urls = set([a.split('&')[0] for a in open('realtorurls.txt')])
	processed = [a for a in open('processed.txt')]
	f = open('processed.txt', 'a')
	for url in urls:
		if url not in processed:
			parserealtor(url)
			f.write(url + '\n')
	f.close()

parseurllist()
