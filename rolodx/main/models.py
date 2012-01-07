from django.db import models

# to consider: should Users just be Pros?  Is Pro even a good name?
#	JS: I had to read around to figure out what 'Pro' meant. Maybe 'Professional' instead? 
#	WRT Professionals and Users, perhaps a Professional can inherit from a User?
#	This would make sense if we'll be having users who have their own business(es)
#	listed on rolodx.

# TODO: we probably need some sort of denormalization of ratings, so getting the average rating of a Pro isn't so slow


class Pro(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	website = models.URLField()
	def __unicode__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Category(models.Model):
	parent = models.ForeignKey('self')
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class ProCategories(models.Model):
	pro = models.ForeignKey(Pro)
	category = models.ForeignKey(Category)

class Rating(models.Model):
	score = models.IntegerField()
	rater = models.ForeignKey(User)
	review = models.TextField()

class ProRatings(models.Model):
	pro = models.ForeignKey(Pro)
	rating = models.ForeignKey(Rating)

