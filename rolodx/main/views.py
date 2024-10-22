import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.backend.ui_models import SearchPageModel, CategoryPageModel, ProfileModel
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService, Order
from backend.categoryservice import CategoryService
import backend.geo
from django.http import HttpResponse
import json
from main.models import UserProfessional
from django.contrib.auth.decorators import login_required

#TODO: We will probably want to consider splitting this file when it gets too big

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

@login_required
def addReview(request, itemId):
	from django.core.serializers import serialize
	professionalId = int(itemId);
	svc = ProfessionalService()
	review = svc.addReview(professionalId, request.user, request.POST.get('rating'), request.POST.get('text'))
	#TODO: status return code *and* new review
	jsonReview = serialize('json', [review,], fields=('date','karma','rating','text', 'user'), relations={'user' : {'fields' : ('username', )} })
	return HttpResponse(jsonReview, mimetype="application/json")

@login_required
def addProfessional(request):
	from django.core.serializers import serialize

	professional = ProfessionalService().addProfessional(
		name = request.POST.get('name'),
		occupation = request.POST.get('occupation'),
		description = request.POST.get('description'),
		email = request.POST.get('email'),
		website = request.POST.get('website'),
		categories = request.POST.get('categories'),
		street_address = request.POST.get('streetaddress'),
		state_province = request.POST.get('stateprovince'),
		country = request.POST.get('country'),
		daytimePhone = request.POST.get('daytimephone'),
		eveningPhone = request.POST.get('eveningphone'),
	)

	#TODO: status return code
	jsonProfessional = serialize('json', [professional, ])
	return HttpResponse(jsonProfessional, mimetype="application/json")

def profile(request):
	user = request.user
	userProfessionals = UserProfessional.objects.filter(user__pk=user.id)
	model = ProfileModel(user.username, user.email, userProfessionals)
	return render_to_response('profile.html', model.json, context_instance=RequestContext(request))

def logout(request):
	from django.http import HttpResponseRedirect
	django.contrib.auth.logout(request)
	return HttpResponseRedirect('/')