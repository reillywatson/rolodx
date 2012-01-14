from haystack.query import SearchQuerySet

class SearchController():    
    def search(self, text):
        result = []
        searchResults = SearchQuerySet().filter(content=text)
        for searchResult in searchResults:
            result.append(searchResult.object)
        return result