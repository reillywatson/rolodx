from main import models
from django.core.serializers import serialize

class SearchPageModel():
    def __init__(self, searchResults):
        self.numResults = len(searchResults)
        self.json = serialize('json', searchResults, fields=('name','occupation','rating','id','description'))
        
        
class ItemPageModel():
    def __init__(self, item):
        self.numComments = 0;   # TODO
        self.json = serialize('json', item, fields=('name','occupation','rating','numRatings','street_address','website','email','description'))
        