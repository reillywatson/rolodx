import haystack
from haystack.query import SearchQuerySet
from ui_models import SearchPageModel

class SearchService:
	
	def ApplyLocationFiltering(self, lat, lng, radius, searchResultsQuery):
		if -90 <= lat <= 90 and -180 <= lng <= 180:
			minlat = lat - radius
			minlng = lng - radius
			maxlat = lat + radius
			maxlng = lng + radius
			print 'range: ', [minlat, minlng], [maxlat, maxlng]
			searchResultsQuery.filter(address_latitude__range=[minlat, maxlat], address_longitude__range=sorted([maxlng, minlng]))

	def search(self, text, lat, lng, radius, currentPage, itemsPerPage):

		# By specifying the exact range of items we want with start and end, we only
		# pull what we need from Solr, instead of getting all items.
		start = (currentPage-1)*itemsPerPage
		end = start+itemsPerPage
		searchResultsQuery = SearchQuerySet().auto_query(text)

		if not lat is None and not lng is None:
			self.ApplyLocationFiltering(lat, lng, radius, searchResultsQuery)

		searchResults = searchResultsQuery[start:end]
		totalResults = searchResultsQuery.count()
		print [(a.address_latitude, a.address_longitude) for a in searchResults[:itemsPerPage]]
		print [(a.object.address_latitude, a.object.address_longitude) for a in searchResults[:itemsPerPage]]

		searchObjects = [a.object for a in searchResults]
		return SearchResult(searchObjects, itemsPerPage, currentPage, totalResults, text)

class SearchResult:
	def __init__(self, searchObjects, itemsPerPage, currentPage, totalResults, text):
		self.searchObjects = searchObjects
		self.itemsPerPage = itemsPerPage
		self.currentPage = currentPage
		self.totalResults = totalResults
		self.text = text
