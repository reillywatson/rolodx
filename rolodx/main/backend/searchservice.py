import haystack
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point

class Order:
	DISTANCE = 1
	RATING = 2

class SearchService:
	
	def ApplyLocationFiltering(self, lat, lng, radius, searchResultsQuery, ordering):
		if -90 <= lat <= 90 and -180 <= lng <= 180:
			topLeft = Point(lng-radius,lat-radius)
			bottomRight = Point(lng+radius,lat+radius)
			
		if ordering == Order.RATING:
			sqs = searchResultsQuery.within('location', topLeft, bottomRight).distance('location', Point(lng,lat)).order_by('-averageRating')
		else:
			sqs = searchResultsQuery.within('location', topLeft, bottomRight).distance('location', Point(lng,lat)).order_by('distance')
		
		return sqs

	def search(self, text, lat, lng, radius, currentPage, itemsPerPage, ordering=Order.RATING):
		# By specifying the exact range of items we want with start and end, we only
		# pull what we need from Solr, instead of getting all items.
		start = (currentPage-1)*itemsPerPage
		end = start+itemsPerPage

		# Filter By Location
		if not lat is None and not lng is None:
			searchResultsQuery = SearchQuerySet().auto_query(text) 
			searchResultsQuery = self.ApplyLocationFiltering(lat, lng, radius, searchResultsQuery, ordering)
		else:	
			searchResultsQuery = SearchQuerySet().auto_query(text).order_by('-averageRating')
		
		# Paginate Results
		searchResults = searchResultsQuery[start:end]
		totalResults = searchResultsQuery.count()

		searchObjects = [a.object for a in searchResults]
		return SearchResult(searchObjects, itemsPerPage, currentPage, totalResults, text)

class SearchResult:
	def __init__(self, searchObjects, itemsPerPage, currentPage, totalResults, text):
		self.searchObjects = searchObjects
		self.itemsPerPage = itemsPerPage
		self.currentPage = currentPage
		self.totalResults = totalResults
		self.text = text
