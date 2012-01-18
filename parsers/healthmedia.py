import re
from pageretriever import PageRetriever
import json

def populate_doctors():
	import os
	import json
	from rolodx.main.models import Professional, Category
	from django.db import transaction
	with transaction.commit_on_success():
		rootCat = Category(name='Doctors', occupation='Doctor')
		rootCat.save()
		# you'll probably need to change this!
		base = '/home/reilly/rolodx/parsers/doctors'
		files = sorted(os.listdir(base))
		for file in files:
			doctors = json.loads(open(base+'/'+file).read())
			print 'found %d doctors in %s' % (len(doctors), file)
			for doc in doctors:
				pro = Professional(
					name = doc['name'].replace('Doctor ', ''),
					occupation = 'Doctor',
					street_address = doc['address'],
					state_province = 'Ontario',
					country = 'Canada',
					daytimePhone = doc['phone'],
					averageRating = 0,
					numRatings = 0)
				pro.save()
				if doc['category'] != 'None':
					category = Category(parent=rootCat, name = doc['category'], occupation = doc['category'])
					category.save()
					pro.categories.add(category)
					pro.save()
	print 'success!'

# this will likely need updating.  Login to ontariodoctordirectory.ca (this may cost you $10!) and copy your cookie data here.
# My account is reillywatson@gmail.com/123456, but it's only good for 1 month.
# If you don't care about specialty information, you don't need to bother logging in, everything else ought to work.
cookie = "__unam=864e7ef-134e8e1f09d-4670959b-1; __utmx=245865818.; __utmxx=245865818.; PHPSESSID=a5b685b5bd5d96b72680f6b96bf4ab3a; __utma=166909665.526384761.1326757732.1326757732.1326757732.1; __utmb=166909665.21.10.1326757732; __utmc=166909665; __utmz=166909665.1326757732.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
getPage = PageRetriever('http://www.ontariodoctordirectory.ca', headers={'Cookie':cookie}).getPage

def tryMatch(pattern, text):
	result = ''
	match = re.search(pattern, text)
	if match != None:
		result = match.group(1).strip()
	return result

def parsedoc(url, city):
	print url
	soup = getPage(url)
	docName = soup.findAll('strong')[1].text
	# take out the "view on map" junk
	if soup.address != None:
		soup.address.div.extract()
		addressComponents = '\n'.join([a for a in soup.address.contents if 'text' not in dir(a)][1:])
	else:
		print "I don't know how to find the address yet!"
		raise ValueException
	phone = tryMatch('Phone:(.*?)\n', soup.prettify())
	fax = tryMatch('Fax:(.*?)\n', soup.prettify())
	specialty = tryMatch('Specialty:(.*?)\n', soup.prettify())
	print "specialty: " + specialty
	return {'name':docName,'address':addressComponents,'phone':phone,'fax':fax, 'category':specialty}


def getcitylist():
	soup = getPage('http://www.ontariodoctordirectory.ca/')
	cities = [x.a for x in soup.find(id='footer').findAll('li')]
	for city in cities:
		cityname = city.text
		cityurl = city['href']
		f = open(cityname+'.txt', 'w')
		jsonarray = []
		docsInCity = parsecity(cityurl)
		for doc in docsInCity:
			jsonarray.append(parsedoc(doc, cityname))
		if len(jsonarray) > 0:
			f.write(json.dumps(jsonarray))

def parsecity(url):
	print 'link: ' + url
	cityUrlPortion = '/'.join(url.split('/')[:2])
	soup = getPage(url)
	docs = [a['href'] for a in soup.findAll(href=re.compile('^'+cityUrlPortion+'/[Dd]octor'))]
	nextPage = soup.find(href=re.compile('^'+cityUrlPortion+'/\\d\\d?'))
	if nextPage != None:
		docs.extend(parsecity(nextPage['href']))
	print 'got %d doctors' % len(docs)
	return docs
