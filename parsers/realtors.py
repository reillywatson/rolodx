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
	links = soup.findAll('a')
	urls = [a['href'] for a in links]
	details = [a for a in urls if 'RealtorDetails' in a]
	nextPage = [a for a in links if a.text == 'Next']
	if len(nextPage) > 0:
		details.extend(getDetails(nextPage[0]['href']))
	return details

def searchsite():
	# let's just use the 100 most common for now
	names = getsurnames()[100:101]
	for name in names:
		details = getDetails('http://www.realtor.ca/REALTORResults.aspx?&lastname=%s&ps=50'%name)
		return details
#		for realtor in details:
#			parseRealtor(realtor)
#		return soup
