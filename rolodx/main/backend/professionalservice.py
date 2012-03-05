from main.models import Professional, Review
from ui_models import ItemPageModel
from datetime import datetime

class ProfessionalService:
	
	def getItemPageData(self, professionalId, currentPage, itemsPerPage):
		items = Professional.objects.filter(pk=professionalId)
		reviews = Review.objects.filter(professional__pk=professionalId)
		return ItemPageModel(items, reviews, itemsPerPage, currentPage)
		
	def addReview(self, professionalId, user, rating, reviewText):
		items = Professional.objects.filter(pk=professionalId)
		if len(items) == 1 and user != None and not user.is_anonymous:
			pro = items[0]
			review = Review(user=user, professional=pro, text=reviewText, rating=rating, date=datetime.utcnow(), karma=0)
			review.save()
