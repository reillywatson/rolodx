from haystack.indexes import *
from haystack import site
from main.models import Professional, Category, Service

class ProfessionalIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	name = CharField(model_attr='name')

	def index_queryset(self):
		"""Used when the entire index for model is updated."""
		return Professional.objects.all()

site.register(Professional, ProfessionalIndex)
