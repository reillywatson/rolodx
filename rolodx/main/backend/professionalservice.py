__author__ = 'Josh'

from main.models import Professional, Review
from main.ui_models import ItemPageModel

class ProfessionalService:
	
	def getItemPageData(self, professionalId, currentPage, itemsPerPage):
		items = Professional.objects.filter(pk=professionalId)
		reviews = Review.objects.filter(professional__pk=professionalId)

		return ItemPageModel(items, reviews, itemsPerPage, currentPage)	