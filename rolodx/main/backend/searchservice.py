from haystack.query import SearchQuerySet

class SearchService:
	# TODO: Paging
	def search(self,text):
		result = []
		searchResults = SearchQuerySet().filter(content=text)
		for searchResult in searchResults:
			result.append(searchResult.object)
		return result
