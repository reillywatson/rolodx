from searchservice import SearchService
from main.models import Category

class CategoryService:
	
	def loadCategory(self, category, lat, lng, radius, currentPage, itemsPerPage):
		#Get the matching category from the database
		if category == "more":
			print "TODO: Deal with 'more' selection"
			categories = []
		else:
			categories = Category.objects.filter(name__iexact=category)
			categories[0].children = Category.objects.filter(parent__exact=categories[0].pk)

		# Get matching professionals
		svc = SearchService()
		searchResult = svc.search(category, lat, lng, radius, currentPage, itemsPerPage)
		
		#Return results
		return CategoryResult(categories, searchResult)
	
class CategoryResult:
	def __init__(self, categories, searchResults):
		self.searchResult = searchResults
		self.categories = categories