from django.db import models

# to consider: should Users just be Pros?
#	WRT Professionals and Users, perhaps a Professional can inherit from a User?
#	This would make sense if we'll be having users who have their own business(es)
#	listed on rolodx.

# reminder: Update admin.py for any new model classes added.

# An arbitrary service which a Professional provides.
class Service(models.Model):
	description = models.TextField()
	def __unicode__(self):
		return self.description

class Category(models.Model):
	parent = models.ForeignKey('self', blank=True, null=True)
	name = models.CharField(max_length=200)
	occupation = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

# If you change fields in the Professional class, you may need to edit
# the Solr schema.xml to match.
class Professional(models.Model):
	name = models.CharField(max_length=200)
	occupation = models.CharField(max_length=200, blank = True, null = True);
	description = models.TextField(blank=True, null=True)
	email = models.CharField(max_length=200)
	website = models.URLField(blank=True, null=True)
	categories = models.ManyToManyField(Category, blank=True, null=True)

	averageRating = models.DecimalField(decimal_places=1, max_digits=2)
	numRatings = models.IntegerField()

	# Contact info
	street_address = models.CharField(max_length=2000, blank=True, null=True)
	state_province = models.CharField(max_length=50, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	daytimePhone = models.CharField(max_length=50, blank=True, null=True)
	eveningPhone = models.CharField(max_length=50, blank=True, null=True)
	address_latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
	address_longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
	#icon?

	# A Professional may offer multiple services. 
	# Multiple Professionals may offer the same services.
	# TODO: Not sure if this is required, needs good example first
	services = models.ManyToManyField(Service, blank=True, null=True)
	def __unicode__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=200)
	external_id = models.CharField(max_length=200)
	# TODO: Other facebook things
	email = models.CharField(max_length=200, blank=True, null=True) #email optional?
	def __unicode__(self):
		return self.name

class Review(models.Model):
	user = models.ForeignKey(User)
	userDisplayName = models.CharField(max_length=200)
	professional = models.ForeignKey(Professional)
	text = models.CharField(max_length=2000)
	rating = models.DecimalField(decimal_places=1, max_digits=2)
	date = models.DateTimeField()
	#If we want to do " x / y found this helpful", we'd need different fields
	karma = models.IntegerField()

class ProfessionalReview(models.Model):
	professional = models.ForeignKey(Professional)
	rating = models.ForeignKey(Review)

class ProfessionalCategory(models.Model):
	professional = models.ForeignKey(Professional)
	category = models.ForeignKey(Category)

class UserProfessional(models.Model):
	user = models.ForeignKey(User)
	professional = models.ForeignKey(Professional)
