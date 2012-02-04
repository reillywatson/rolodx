from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category
from backend.professionalservice import ProfessionalService
from backend.searchservice import SearchService
import decimal

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def search(request):
	# Get request parameters
	query = request.GET['q']
	lat = request.GET.get('lat', '1000')
	long = request.GET.get('lng', '1000')
	clientLatitude = None if lat == u'' else decimal.Decimal(lat)
	clientLongitude = None if lat == u'' else decimal.Decimal(long)
	searchRadius = decimal.Decimal(request.GET.get('radius', '2'))
	currentPage = int(request.GET.get('p','1'))
	itemsPerPage = int(request.GET.get('n','7')) #TODO: This should probably not be here. We don't want users to control our pagination.
	
	# Get data from backend, based on request
	svc = SearchService()
	model = svc.search(query, clientLatitude, clientLongitude, searchRadius, currentPage, itemsPerPage)
	
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
	model = svc.getItemPageData(professionalId, currentPage, itemsPerPage)
	
	# Return response to the client
	clientData = {"results" : model.json}
	return render_to_response('item.html', clientData, context_instance=RequestContext(request))


# TODO: The following will need to be revisited when we work on categories
def search_category(request):
	categories = Category.objects.filter(name__contains=request.POST['category'])
	return display_categories(request, categories)

def category(request, category_name):
	categories = Category.objects.filter(name__contains=category_name)
	return display_categories(request, categories)

def display_categories(request, categories):
	if len(categories) > 0:
		dictionary = {'num_results':len(categories), 'categories':categories}
		return render_to_response('category.html', dictionary, context_instance=RequestContext(request))
	else:
		return render_to_response('category.html', {'error_message':'No results found'}, context_instance=RequestContext(request))
