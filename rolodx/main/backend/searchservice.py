import haystack
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point

class Order:
	DISTANCE = 1
	RATING = 2

class SearchService:
	def search(self, text, lat, lng, radius, currentPage, itemsPerPage, ordering=Order.RATING):
		print 'searching!'
		print (lat,lng,radius)
		# By specifying the exact range of items we want with start and end, we only
		# pull what we need from Solr, instead of getting all items.
		start = (currentPage-1)*itemsPerPage
		end = start+itemsPerPage

		# Filter By Location
		query = SearchQuerySet().auto_query(text)
		if -90 <= lat <= 90 and -180 <= lng <= 180:
			topLeft = Point(lng-radius,lat-radius)
			bottomRight = Point(lng+radius,lat+radius)
			query = query.within('location', topLeft, bottomRight).distance('location', Point(lng,lat))
			if ordering == Order.DISTANCE:
				query = query.order_by('distance')
		if ordering == Order.RATING:
			query = query.order_by('-averageRating')
		
		# Paginate Results
		searchResults = query[start:end]
		totalResults = query.count()

		searchObjects = [a.object for a in searchResults]
		return SearchResult(searchObjects, itemsPerPage, currentPage, totalResults, text)

class SearchResult:
	def __init__(self, searchObjects, itemsPerPage, currentPage, totalResults, text):
		self.searchObjects = searchObjects
		self.itemsPerPage = itemsPerPage
		self.currentPage = currentPage
		self.totalResults = totalResults
		self.text = text
