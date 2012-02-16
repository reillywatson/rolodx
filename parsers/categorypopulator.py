from main.models import Category
from datetime import datetime

topLevelCategories = ['Health', 'Home', 'Finance', 'Technology', 'Personal Care']
subcategories = { 
					'Health' : ['Doctor', 'Dentist', 'Therapist', 'Optometrist', 'Personal Trainer'],
					'Home' : ['Real Estate Agent', 'Home Inspector', 'Interior Designer', 'Carpenter', 'Handy Man'],
					'Finance' : ['Accountant', 'Lawyer', 'Mortgage Broker', 'Financial Advisor', 'Notary'],
					'Technology' : ['Computer Repair'],
					'Personal Care' : ['Barber', 'Hair Dresser', 'Masseuse']
				}


class CategoryPopulator:
	def recursively_delete_category(self, category):
		if category.children is not None:
			for child in category.children.all():
				self.recursively_delete_category(child)
				child.delete()

	def create_category(self, categoryName):
		#TODO: Occupation?
		parent = Category(name=categoryName, occupation=categoryName)
		parent.save()

		subcategoryList = subcategories[categoryName]
		for subcategoryName in subcategoryList:
			child = Category(name=subcategoryName, occupation=subcategoryName, parent=parent)
			child.save()
			parent.children.add(child)

		parent.save()
	
	def populate_categories(self):

		# First populate top level categories
		for categoryName in topLevelCategories:
			existing = Category.objects.filter(name__iexact=categoryName).all()
			if len(existing) == 0:
				self.create_category(categoryName)
				print 'Created category %s' % (categoryName)
			else:
				print 'Category %s exists, deleting and recreating' % (categoryName)
				for e in existing:
					self.recursively_delete_category(e)
					e.delete()
				self.create_category(categoryName)


populator = CategoryPopulator()
populator.populate_categories()
