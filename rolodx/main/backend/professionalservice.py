from main.models import Professional, Review, UserProfessional
from main.search_indexes import ProfessionalIndex
from ui_models import ItemPageModel
from datetime import datetime

class ProfessionalService:
	
	def getItemPageData(self, professionalId, currentPage, itemsPerPage):
		items = Professional.objects.filter(pk=professionalId)
		reviews = Review.objects.filter(professional__pk=professionalId).order_by('-date')
		return ItemPageModel(items, reviews, itemsPerPage, currentPage)
		
	def addReview(self, professionalId, user, rating, reviewText):
		#TODO: fix js to always send a number for rating?
		# RB: Yes. But we should have this as a backup anyway.
		if rating == 'null':
			rating = 0

		items = Professional.objects.filter(pk=professionalId)
		if len(items) == 1 and user != None and not user.is_anonymous():
			professional = items[0]

			reviews = Review.objects.filter(professional=professional, user=user)
			if len(reviews) != 0:
				# Update review/rating
				review = reviews[0]
				review.rating = rating
				review.date = datetime.utcnow()
				review.text=reviewText
				print review.text, review.rating, review.date
			else:
				# Add new review/rating
				review = Review(user=user, professional=professional, text=reviewText, rating=rating, date=datetime.utcnow(), karma=0)

				# Create association
				association = UserProfessional(user=user, professional=professional)
				association.save()

			review.save()

			# Create association
			association = UserProfessional(user=user, professional=items[0])
			association.save()

		return review

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

	#TODO: should we link an added professional to the user that created it?
	def addProfessional(self, name, occupation, description, email, website, categories,
	                    street_address, state_province, country, daytimePhone, eveningPhone):
		from haystack import indexes

		professional = Professional()
		professional.name = name
		professional.occupation = occupation
		professional.description = description
		professional.email = email
		professional.website = website
		#professional.categories = categories
		professional.street_address = street_address
		professional.state_province = state_province
		professional.country = country
		professional.daytimePhone = daytimePhone
		professional.eveningPhone = eveningPhone

		now = datetime.utcnow()
		professional.dateCreated = now
		professional.lastModified = now

		professional.averageRating = 0
		professional.numRatings = 0

		professional.save()

		# TODO: somehow update solr asynchronously? Synchronous update for now ...
		index = ProfessionalIndex()
		index.update_object(instance=professional)

		return professional