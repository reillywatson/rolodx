from django.db import models

# to consider: should Users just be Pros?
#	WRT Professionals and Users, perhaps a Professional can inherit from a User?
#	This would make sense if we'll be having users who have their own business(es)
#	listed on rolodx.

# TODO: we probably need some sort of denormalization of ratings, so getting the average rating of a Pro isn't so slow

# reminder: Update admin.py for any new model classes added.

# An arbitrary service which a Professional provides.
class Service(models.Model):
	description = models.TextField()
	def __unicode__(self):
		return self.description

class Professional(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	website = models.URLField()
	# A Professional may offer multiple services. 
	# Multiple Professionals may offer the same services.
	services = models.ManyToManyField(Service)
	def __unicode__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Category(models.Model):
	parent = models.ForeignKey('self', blank=True, null=True)
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class ProfessionalCategory(models.Model):
	professional = models.ForeignKey(Professional)
	category = models.ForeignKey(Category)

class Rating(models.Model):
	score = models.IntegerField()
	rater = models.ForeignKey(User)
	review = models.TextField()

class ProfessionalRating(models.Model):
	professional = models.ForeignKey(Professional)
	rating = models.ForeignKey(Rating)

#
