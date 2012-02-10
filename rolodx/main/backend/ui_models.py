import json
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

# Right now, these model classes assume they always return JSON data.
# But it's not hard to change, if we change our minds.
class SearchPageModel():
	def __init__(self, searchResults, itemsPerPage, currentPage, totalResults, searchQuery):

		numPages = max(totalResults / itemsPerPage, 1)
		serializedResults = serialize('json', searchResults, fields=('name','occupation','averageRating','description', 'numRatings', 'address_latitude', 'address_longitude'))
		serializedPaging = {"currentPage": currentPage, "numPages" : numPages}

		self.json = {'searchResults' : serializedResults, 'paging' : serializedPaging, 'searchquery' : searchQuery}


class ItemPageModel():
	def __init__(self, item, reviews, itemsPerPage, pageNum):
		paginator = Paginator(reviews, itemsPerPage)
		page = getpage(paginator, pageNum)
		
		serializedItem = serialize('json', item, fields=('name','occupation','averageRating','numRatings','street_address','website','email','description', 'address_latitude', 'address_longitude'))
		serializedReviews = serialize('json', page.object_list,  fields=('date','karma','rating','text', 'userDisplayName'))
		serializedPaging = {"currentPage": page.number, "numPages" : paginator.num_pages}
		
		self.json = {"itemData" : serializedItem, "reviews" : serializedReviews, "paging" : serializedPaging}

class CategoryPageModel():
	def __init__(self, categories, searchResult):
		# We should only have one matching category name ...
		print "-----------------------"
		print categories
		category = categories[0]
		
		searchModel = SearchPageModel(searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)

		subcategoryNames = []
		for subcategory in category.children.all():
			subcategoryNames.append(subcategory.name)

		self.json = {
			'category':serialize('json', [category], fields=("name")),
			'subcategoryNames':json.dumps(subcategoryNames),
			'results':searchModel .json
		}