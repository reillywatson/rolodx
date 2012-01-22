from main import models
from django.core.serializers import serialize

class SearchPageModel():
    def __init__(self, searchResults, pageData, searchQuery):
        self.numResults = len(searchResults)
        serializedResults = serialize('json', searchResults, fields=('name','occupation','averageRating','description', 'numRatings', 'address_latitude', 'address_longitude'))
        self.json = {'searchResults' : serializedResults, 'pagedata' : pageData, 'searchquery' : searchQuery}
        
        
class ItemPageModel():
    def __init__(self, item):
        self.numComments = 0;   # TODO
        self.json = serialize('json', item, fields=('name','occupation','averageRating','numRatings','street_address','website','email','description', 'address_latitude', 'address_longitude'))
        
