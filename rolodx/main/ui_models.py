from main import models

class SearchPageModel():
    def __init__(self, searchResults):
        self.numResults = len(searchResults)
        self.json = "["
        for result in searchResults:
            self.json += "{"
            self.json += "\"name\" : \"" + result.name + "\", "
            self.json += "\"id\" : \"" + str(result.id) + "\", "
            self.json += "\"occupation\" : \"" + result.occupation + "\", "
            self.json += "\"description\" : \"" + str(result.description) + "\", "
            # TODO: self.json += "\"icon\" : \"" + str(result.icon) + "\","
            self.json += "\"rating\" : \"" + str(result.averageRating) + "\""
            
            self.json += "},"
        self.json += "]"
        
        
class ItemPageModel():
    def __init__(self, item):
        self.numComments = 0;   # TODO
        self.json = "{"
        self.json += "\"name\" : \"" + item.name + "\", "
        self.json += "\"occupation\" : \"" + item.occupation + "\", "
        self.json += "\"rating\" : \"" + str(item.averageRating) + "\", "
        self.json += "\"numRatings\" : \"" + str(item.numRatings) + "\", "
        self.json += "\"street_address\" : \"" + str(item.street_address).replace("\n", " ") + "\", "
        self.json += "\"website\" : \"" + str(item.website) + "\", "
        self.json += "\"email\" : \"" + str(item.email) + "\", "
        #TODO: self.json += "\"hours\" : \"" + str(item.hours) + "\", "
        self.json += "\"description\" : \"" + str(item.description) + "\", "
        # TODO: self.json += "\"icon\" : \"" + str(result.icon) + "\" "
        self.json += "}"
    