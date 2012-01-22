from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category, Professional
from ui_models import SearchPageModel, ItemPageModel
from controllers.search_controller import SearchController
from django.core.serializers import serialize

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def clamp(minval, n, maxval):
	return max(minval, min(n, maxval))

def search(request):
	pagedata = SearchController().search(request.GET['q'], int(request.GET.get('p','1')), int(request.GET.get('n','7')))
	searchModel = SearchPageModel([a.object for a in pagedata.object_list]).json
	return render_to_response('search.html', {'results' : searchModel, 'pagedata' : pagedata, 'searchquery' : request.GET['q']}, context_instance=RequestContext(request))

def item(request, itemId):
	items = Professional.objects.filter(pk=int(itemId))
	itemModel = ItemPageModel(items).json
	results = {"itemData" : itemModel, "reviews" : []}
	return render_to_response('item.html', {"results" : results}, context_instance=RequestContext(request))

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

	
