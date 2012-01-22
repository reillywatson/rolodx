import haystack
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def getpage(paginator, page):
	try:
		results = paginator.page(page)
	except PageNotAnInteger:
		results = paginator.page(1)
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
	return results

class SearchService:
	def search(self,text,lat,lng,radius,page,items_per_page):
		searchResults = SearchQuerySet().auto_query(text)
		if -90 <= lat <= 90 and -180 <= lng <= 180:
			minlat = lat - radius
			minlng = lng - radius
			maxlat = lat + radius
			maxlng = lng + radius
			print 'range: ', [minlat,minlng],[maxlat,maxlng]
			searchResults.filter(address_latitude__range=[minlat,maxlat], address_longitude__range=sorted([maxlng,minlng]))
		print [(a.address_latitude, a.address_longitude) for a in searchResults[:items_per_page]]
		print [(a.object.address_latitude, a.object.address_longitude) for a in searchResults[:items_per_page]]
		# HACK: iterate over the search results in order for pagination to
		# work.  This can be removed when we have SOLR set up, this is a 
		# bug in Haystack's simple backend (see https://github.com/toastdriven/django-haystack/issues/320)
		if haystack.backend.__name__ == 'haystack.backends.simple_backend':
			[a for a in searchResults]

		paginator = Paginator(searchResults, items_per_page)
		return getpage(paginator, page)
