from django.shortcuts import render_to_response
from django.template import RequestContext
from main.backend.ui_models import SearchPageModel, CategoryPageModel
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService, Order
from backend.categoryservice import CategoryService
import backend.geo
from django.conf import settings

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

#Returns a dictionary of search/location related querystring parameters
def getQuerystringParameters(request):
	# Get request parameters
	query = request.GET.get('q', None)
	useLocation = request.GET.get('useLocation', "1");
	sort = request.GET.get('sort', 1);
	clientLatitude = None
	clientLongitude = None

	print "_______________"
	print useLocation

	latLong = None;
	if useLocation == "1":
		print "USING LOCATION"
		latLong = backend.geo.lookup(request.META['REMOTE_ADDR'])
		if latLong != None:
			clientLatitude = latLong[0]
			clientLongitude = latLong[1]
			
	searchRadius = float(request.GET.get('radius', '.2'))
	currentPage = int(request.GET.get('p', '1'))
	itemsPerPage = int(request.GET.get('n',
									   '7')) #TODO: This should probably not be here. We don't want users to control our pagination.
	return {
		'lat' : clientLatitude,
		'long' : clientLongitude,
		'currentPage' : currentPage,
		'itemsPerPage' : itemsPerPage,
		'query' : query,
		'searchRadius' : searchRadius,
		'useLocation' : useLocation,
		'sort' : sort
	}

def search(request):
	params = getQuerystringParameters(request)
	ordering = Order.RATING
	if params['sort'] == "2":
		ordering = Order.DISTANCE
	searchResult = SearchService().search(params['query'], params['lat'], params['long'], params['searchRadius'], params['currentPage'], params['itemsPerPage'], ordering)
	model = SearchPageModel(params["useLocation"], params["sort"], searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)

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
	print "================================"
	print clientData
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
		model = CategoryPageModel(params["useLocation"], params["sort"], categories, searchResult)
		print "--------------------" 
		print model.json
		return render_to_response('category.html', model.json, context_instance=RequestContext(request))
	else:
		return render_to_response('category.html', {'error_message':'No results found'}, context_instance=RequestContext(request))
