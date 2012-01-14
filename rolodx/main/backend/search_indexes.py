from haystack.indexes import *
from haystack import site
from main.models import Professional, Category, Service

class ProfessionalIndex(SearchIndex):
	text = CharField(document=True, use_template=True)

site.register(Professional, ProfessionalIndex)
