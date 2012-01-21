from haystack.query import SearchQuerySet

#TODO: Do we still need this?
from rolodx.main.backend.searchservice import SearchService

class SearchController():
	def search(self, text, page, items_per_page):
		return SearchService().search(text, page, items_per_page)
