import BeautifulSoup
import requests

class PageRetriever:
	baseUrl = ''
	def __init__(self, baseUrl):
		self.baseUrl = baseUrl
	def getPage(self, url):
		if not url.startswith('http'):
			url = self.baseUrl + url
		print 'retrieving: ' + url
		url = url.replace(' ', '%20')
		tries = 0
		while tries < 3:
			response = requests.get(url)
			if response.status_code == 200:
				return BeautifulSoup.BeautifulSoup(response.content)
			print 'failed with error %d, retrying!' % response.status_code
			time.sleep(1)
			tries = tries + 1
		return None
