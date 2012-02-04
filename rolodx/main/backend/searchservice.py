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
		self.ApplyLocationFiltering(lat, lng, radius, searchResultsQuery)

		searchResults = searchResultsQuery[start:end]
		totalResults = searchResultsQuery.count()
		print [(a.address_latitude, a.address_longitude) for a in searchResults[:itemsPerPage]]
		print [(a.object.address_latitude, a.object.address_longitude) for a in searchResults[:itemsPerPage]]
		# HACK: iterate over the search results in order for pagination to
		# work.  This can be removed when we have SOLR set up, this is a 
		# bug in Haystack's simple backend (see https://github.com/toastdriven/django-haystack/issues/320)
		if haystack.backend.__name__ == 'haystack.backends.simple_backend':
			[a for a in searchResults]

		searchObjects = [a.object for a in searchResults]
		return SearchPageModel(searchObjects, itemsPerPage, currentPage, totalResults, text)
