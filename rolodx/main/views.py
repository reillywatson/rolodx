from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import Category
from backend.search_controller import SearchController
from django.core.serializers import serialize
from django.utils import simplejson

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def search(request):
	results = SearchController().search(request.GET['q']);
	print serialize('json', results)
	return render_to_response('search.html', {'results' : serialize('json', results)}, context_instance=RequestContext(request))

def item(request):
	return render_to_response('item.html', context_instance=RequestContext(request))

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

	
