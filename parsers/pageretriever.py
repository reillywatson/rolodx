import BeautifulSoup
import requests

class PageRetriever:
	baseUrl = ''
	args = {}
	def __init__(self, baseUrl, **kwargs):
		self.baseUrl = baseUrl
		self.args = kwargs
	def getPage(self, url, **kwargs):
		if not url.startswith('http'):
			url = self.baseUrl + url
		print 'retrieving: ' + url
		url = url.replace(' ', '%20')
		tries = 0
		while tries < 3:
			arguments = dict(kwargs.items() + self.args.items())
			response = requests.get(url, **arguments)
			if response.status_code == 200:
				return response.content
			print 'failed with error %d, retrying!' % response.status_code
			time.sleep(1)
			tries = tries + 1
		return None
	def getPageSoup(self, url, **kwargs):
		return BeautifulSoup.BeautifulSoup(self.getPage(url, **kwargs))

