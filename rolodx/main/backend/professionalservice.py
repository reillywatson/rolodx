from main.models import Professional, Review, UserProfessional
from ui_models import ItemPageModel
from datetime import datetime

class ProfessionalService:
	
	def getItemPageData(self, professionalId, currentPage, itemsPerPage):
		items = Professional.objects.filter(pk=professionalId)
		reviews = Review.objects.filter(professional__pk=professionalId)
		return ItemPageModel(items, reviews, itemsPerPage, currentPage)
		
	def addReview(self, professionalId, user, rating, reviewText):
		#TODO: should check if user has already rated this professional, error if this is the case
		#(should edit instead)

		#TODO: fix js to always send a number for rating?
		if rating == 'null':
			rating = 0

		items = Professional.objects.filter(pk=professionalId)
		if len(items) == 1 and user != None and not user.is_anonymous():
			review = Review(user=user, professional=items[0], text=reviewText, rating=rating, date=datetime.utcnow(), karma=0)
			review.save()
			
			# Create association
			association = UserProfessional(user=user, professional=items[0])
			association.save()

	def updateReview(self, professionalId, userId, rating, reviewText):
		reviews = Review.objects.filter(professional__pk=professionalId, user__pk=userId)
		if len(reviews) == 0:
			print 'Review for professional %s and user %s does not exist', (professionalId, userId)
			return
		elif len(reviews) > 1:
			print 'More than one review found for professional %s and user %s does not exist', (professionalId, userId)
			return

		review = reviews[0];
		review.rating = rating;
		review.text = reviewText;
		review.date = datetime.utcnow()
		review.hasBeenModified = False
		review.save()
