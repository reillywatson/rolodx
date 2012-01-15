from haystack.query import SearchQuerySet

#TODO: Do we still need this?
from rolodx.main.backend.searchservice import SearchService

class SearchController():
    def search(self, text):
        return SearchService().search(text)