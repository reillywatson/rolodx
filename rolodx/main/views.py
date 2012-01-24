from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category, Professional, Review
from ui_models import SearchPageModel, ItemPageModel
from controllers.search_controller import SearchController

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def search(request):
	pagedata = SearchController().search(request.GET['q'], int(request.GET.get('p','1')), int(request.GET.get('n','7')))
	searchModel = SearchPageModel([a.object for a in pagedata.object_list], pagedata, request.GET['q']).json
	return render_to_response('search.html', {'results' : searchModel}, context_instance=RequestContext(request))

def item(request, itemId):
	currentPage = int(request.GET.get('p','1'))
	itemsPerPage = int(request.GET.get('n','7'))
	
	items = Professional.objects.filter(pk=int(itemId))
	reviews = Review.objects.filter(professional__pk=int(itemId))
	itemModel = ItemPageModel(items, reviews, itemsPerPage, currentPage).json
	return render_to_response('item.html', {"results" : itemModel}, context_instance=RequestContext(request))


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

	
