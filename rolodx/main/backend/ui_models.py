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

class ItemPageModel():
	def __init__(self, item, reviews, itemsPerPage, pageNum):
		paginator = Paginator(reviews, itemsPerPage)
		page = getpage(paginator, pageNum)
		
		serializedItem = serialize('json', item, fields=('name','occupation','averageRating','numRatings','street_address','website','email','description', 'address_latitude', 'address_longitude'))
		serializedReviews = serialize('json', page.object_list, fields=('date','karma','rating','text', 'user'), relations={'user' : {'excludes' : ('pk', 'model') , 'fields' : ('username', )} }, indent=4)
		print serializedReviews
		serializedPaging = {"currentPage": page.number, "numPages" : paginator.num_pages}
		
		self.json = {"itemData" : serializedItem, "reviews" : serializedReviews, "paging" : serializedPaging}

class BaseModel(object):
	def __init__(self, loc, s):
		self.useLocation = loc
		self.sort = s
		
	def json(self):
		return {'baseData' : json.dumps({'locationBased' : self.useLocation, 'sort' : self.sort}) }

class ProfileModel():
	def __init__(self, userName, userEmail, userProfessionals):
		professionals = []
		for userPro in userProfessionals:
			professionals.append(userPro.professional)
		
		results = {"name" : json.dumps(userName), "email" : json.dumps(userEmail), "professionals" : serialize('json', professionals, fields=('name','occupation','averageRating','description', 'numRatings', 'address_latitude', 'address_longitude')) }
		self.json = {'results' : {"profile" : results}}

class SearchPageModel(BaseModel):
	def __init__(self, useLocation, sort, searchResults, itemsPerPage, currentPage, totalResults, searchQuery):
		super(SearchPageModel, self).__init__(useLocation, sort)
		numPages = max(totalResults / itemsPerPage, 1)
		serializedResults = serialize('json', searchResults, fields=('name','occupation','averageRating','description', 'numRatings', 'address_latitude', 'address_longitude'))
		serializedPaging = {"currentPage": currentPage, "numPages" : numPages}

		result = {'searchResults' : serializedResults, 'paging' : serializedPaging, 'searchquery' : searchQuery}
		self.json = dict(super(SearchPageModel,self).json(), **result)

class CategoryPageModel():
	def __init__(self, useLocation, sort, categories, searchResult):
		# We should only have one matching category name ...
		print "-----------------------"
		print categories
		category = categories[0]
		
		searchModel = SearchPageModel(useLocation, sort, searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)

		subcategoryNames = []
		for subcategory in category.children.all():
			subcategoryNames.append(subcategory.name)
		
		self.json = {
			'category':serialize('json', [category], fields=("name")),
			'subcategoryNames':json.dumps(subcategoryNames),
			'results':searchModel.json
		}
