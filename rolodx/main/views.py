from django.shortcuts import render_to_response
from django.template import RequestContext
from main.backend.ui_models import SearchPageModel
from models import Category
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService
import decimal

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

#Returns a dictionary of search/location related querystring parameters
def getQuerystringParameters(request):
	# Get request parameters
	query = request.GET.get('q', None)
	lat = request.GET.get('lat', '1000')
	long = request.GET.get('lng', '1000')
	clientLatitude = None if lat == u'' else decimal.Decimal(lat)
	clientLongitude = None if lat == u'' else decimal.Decimal(long)
	searchRadius = decimal.Decimal(request.GET.get('radius', '2'))
	currentPage = int(request.GET.get('p', '1'))
	itemsPerPage = int(request.GET.get('n',
									   '7')) #TODO: This should probably not be here. We don't want users to control our pagination.
	return {
		'lat' : clientLatitude,
		'long' : clientLongitude,
		'currentPage' : currentPage,
		'itemsPerPage' : itemsPerPage,
		'query' : query,
		'searchRadius' : searchRadius
	}

def search(request):
	params = getQuerystringParameters(request)
	searchResult = SearchService().search(params['query'], params['lat'], params['long'], params['searchRadius'], params['currentPage'], params['itemsPerPage'])
	model = SearchPageModel(searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)

	# Return response to the client
	clientData = {"results" : model.json}
	return render_to_response('search.html', clientData, context_instance=RequestContext(request))

def item(request, itemId):
	# Get request parameters
	professionalId = int(itemId)
	currentPage = int(request.GET.get('p','1'))
	itemsPerPage = int(request.GET.get('n','7')) #TODO: This should probably not be here. We don't want users to control our pagination.
	
	# Get data from backend, based on request
	svc = ProfessionalService()
	# TODO:JS: I don't think services should be returning page Model objects ...
	model = svc.getItemPageData(professionalId, currentPage, itemsPerPage)
	
	# Return response to the client
	clientData = {"results" : model.json}
	return render_to_response('item.html', clientData, context_instance=RequestContext(request))

def search_category(request):
	categories = Category.objects.filter(name__contains=request.POST['category'])
	return display_categories(request, categories)

def category(request, category_name):
	#Get the matching category from the database
	categories = Category.objects.filter(name__iexact=category_name)
	#Get any matching professionals from search
	params = getQuerystringParameters(request)
	params['query'] = category_name #Set query here, instead of using 'q' from a querystring.
	searchResult = SearchService().search(params['query'], params['lat'], params['long'], params['searchRadius'], params['currentPage'], params['itemsPerPage'])
	return display_categories(request, categories, searchResult)

def display_categories(request, categories, searchResult):
	model = SearchPageModel(searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)
	# We should only have one matching category name ...
	
	print "-----------------------"
	print categories
	
	if len(categories) > 0:
		category = categories[0]

		subcategoryNames = []
		for subcategory in category.children.all():
			subcategoryNames.append(subcategory.name)

		dictionary = {
			'category':category,
			'subcategoryNames':subcategoryNames,
			'results':model.json
		}
		return render_to_response('category.html', dictionary, context_instance=RequestContext(request))
	else:
		return render_to_response('category.html', {'error_message':'No results found'}, context_instance=RequestContext(request))
