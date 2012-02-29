from main.models import Professional, Review, User
from ui_models import ItemPageModel
from datetime import datetime

class ProfessionalService:
	
	def getItemPageData(self, professionalId, currentPage, itemsPerPage):
		items = Professional.objects.filter(pk=professionalId)
		reviews = Review.objects.filter(professional__pk=professionalId)

		return ItemPageModel(items, reviews, itemsPerPage, currentPage)
		
	def addReview(self, professionalId, userId, rating, reviewText):
		items = Professional.objects.filter(pk=professionalId)
		users = User.objects.filter(pk=userId)
		if len(items) == 1 and len(users) == 1:
			pro = items[0]
			user = users[0]
			review = Review(user=user, professional=pro, text=reviewText, rating=rating, date=datetime.utcnow(), karma=0)
			review.save()
