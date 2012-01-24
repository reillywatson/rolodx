from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def getpage(paginator, page):
	try:
		results = paginator.page(page)
	except PageNotAnInteger:
		results = paginator.page(1)
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
	return results

class SearchPageModel():
	def __init__(self, searchResults, pageData, searchQuery):
		serializedResults = serialize('json', searchResults, fields=('name','occupation','averageRating','description', 'numRatings', 'address_latitude', 'address_longitude'))
		self.json = {'searchResults' : serializedResults, 'pagedata' : pageData, 'searchquery' : searchQuery}


class ItemPageModel():
	def __init__(self, item, reviews, itemsPerPage, page):
		paginator = Paginator(reviews, itemsPerPage)
		page = getpage(paginator, page)
		serializedItem = serialize('json', item, fields=('name','occupation','averageRating','numRatings','street_address','website','email','description', 'address_latitude', 'address_longitude'))
		serializedReviews = serialize('json', page.object_list,  fields=('date','karma','rating','text', 'userDisplayName'))
		
		self.json = {"itemData" : serializedItem, "reviews" : serializedReviews, "currentPage" : page.number, "numPages" : paginator.num_pages}
