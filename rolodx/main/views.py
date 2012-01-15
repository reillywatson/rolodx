from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category
from controllers.search_controller import SearchController
from django.core.serializers import serialize

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

#TODO: Do we need to send results as json?
def search(request):
	results = SearchController().search(request.GET['q']);
	print serialize('json', results)
	return render_to_response('search.html',
								{'jsonresults' : serialize('json', results), 'results' : results},
							  context_instance=RequestContext(request))

def item(request, itemId):
	# TODO: Get the professional by ID
	itemData = {
				'name' : 'Robert LeMan Beghian', 
				"job" : "Senior Co-Op Student", 
				"rating" : "0.5", 
				"numRatings" : "53", 
				"address" : "123 Fake Street, Springfield, ON.",
				"description" :  "Bacon ipsum dolor sit amet swine drumstick cow, ham ribeye meatball pork loin kielbasa ground round bacon prosciutto bresaola strip steak chuck chicken. Hamburger spare ribs shankle chuck turducken jowl, ribeye pork drumstick turkey bacon shank short ribs andouille. Pig hamburger ham hock t-bone, tri-tip chuck biltong ham. Pork loin tenderloin pancetta, ribeye jerky short ribs pork belly leberkase biltong kielbasa pork chop frankfurter tri-tip filet mignon. Meatball beef pork belly prosciutto filet mignon tongue. Pork belly biltong sirloin, rump meatball boudin kielbasa shank ham turkey beef pancetta pork chop venison. Salami pastrami leberkase frankfurter cow.",
				"website" : "http://uh.oh", 
				"email" : "spam@me.com", 
				"hours" : "8PM - 3AM"}
			
	results = {"itemData" : itemData, "reviews" : []}
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

	
