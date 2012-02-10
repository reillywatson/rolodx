from django.shortcuts import render_to_response
from django.template import RequestContext
from main.backend.ui_models import SearchPageModel, CategoryPageModel
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService
from backend.categoryservice import CategoryService
import decimal

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

#Returns a dictionary of search/location related querystring parameters
def getQuerystringParameters(request):
	# Get request parameters
	query = request.GET.get('q', None)
	lat = request.GET.get('lat', '1000')
	lng = request.GET.get('lng', '1000')
	clientLatitude = None if lat == u'' else decimal.Decimal(lat)
	clientLongitude = None if lat == u'' else decimal.Decimal(lng)
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

def category(request, category_name):
	#Get any matching professionals from search
	params = getQuerystringParameters(request)
	params['query'] = category_name #Set query here, instead of using 'q' from a querystring.
	
	svc = CategoryService()
	categoryResults = svc.loadCategory(params['query'], params['lat'], params['long'], params['searchRadius'], params['currentPage'], params['itemsPerPage'])
	
	categories = categoryResults.categories
	searchResult = categoryResults.searchResult
	
	if len(categories) > 0:
		model = CategoryPageModel(searchResult, categories)
		return render_to_response('category.html', model.json, context_instance=RequestContext(request))
	else:
		return render_to_response('category.html', {'error_message':'No results found'}, context_instance=RequestContext(request))
