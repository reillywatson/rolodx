import json
import django
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from main.backend.ui_models import SearchPageModel, CategoryPageModel
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService, Order
from backend.categoryservice import CategoryService
from socialregistration.contrib.facebook.middleware import FacebookMiddleware
import backend.geo
from django.conf import settings
from django.http import HttpResponse, HttpRequest
import json
from main.models import UserProfile, UserProfessional

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

	latLong = None;
	if useLocation == "1":
		latLong = backend.geo.lookup(request.META['REMOTE_ADDR'])
		if latLong != None:
			clientLatitude = latLong[0]
			clientLongitude = latLong[1]
			
	searchRadius = float(request.GET.get('radius', '.2'))
	currentPage = int(request.GET.get('p', '1'))
	itemsPerPage = int(request.GET.get('n',
									   '7')) #TODO: This should probably not be here. We don't want users to control our pagination.
	nbound = float(request.GET.get('nbound', 0))
	sbound = float(request.GET.get('sbound', 0))
	ebound = float(request.GET.get('ebound', 0))
	wbound = float(request.GET.get('wbound', 0))
	dataonly = request.GET.get('dataonly', False)
	return {
		'lat' : clientLatitude,
		'long' : clientLongitude,
		'currentPage' : currentPage,
		'itemsPerPage' : itemsPerPage,
		'query' : query,
		'searchRadius' : searchRadius,
		'useLocation' : useLocation,
		'sort' : sort,
		'nbound' : nbound,
		'sbound' : sbound,
		'ebound' : ebound,
		'wbound' : wbound,
		'dataonly' : dataonly
	}

def search(request):
	params = getQuerystringParameters(request)
	ordering = Order.RATING
	if params['sort'] == "2":
		ordering = Order.DISTANCE
	searchResult = SearchService().search(params['query'], params['lat'], params['long'], params['searchRadius'], params['currentPage'], 
										params['itemsPerPage'], ordering, params['nbound'], params['sbound'], params['ebound'], params['wbound'])
	model = SearchPageModel(params["useLocation"], params["sort"], searchResult.searchObjects, searchResult.itemsPerPage, searchResult.currentPage, searchResult.totalResults, searchResult.text)

	# Return response to the client
	clientData = {"results" : model.json}
	
	if (params['dataonly']) :
		return HttpResponse(json.dumps(clientData))
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

def addReview(request, itemId):
	professionalId = int(itemId);
	svc = ProfessionalService()
	svc.addReview(professionalId, request.user, request.POST.get('rating'), request.POST.get('text'))
	resp = {'status':'ok'}
	return HttpResponse(json.dumps(resp), mimetype="application/json")

def profile(request):
	user = request.user
	userProfessionals = UserProfessional.objects.filter(user__pk=user.id)
	clientData = { "username" : user.username,
			"email" : user.email,
			"professionals" : userProfessionals }

	return render_to_response('profile.html', clientData, context_instance=RequestContext(request))

def logout(request):
	from django.http import HttpResponseRedirect
	django.contrib.auth.logout(request)
	return HttpResponseRedirect('/')