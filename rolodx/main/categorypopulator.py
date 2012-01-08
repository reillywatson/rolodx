from main.models import Professional, User, Category, ProfessionalCategory, Rating, ProfessionalRating, Service


class CategoryPopulator:
	def populate_test_categories(self):
		# Root categories
		auto = Category(name="Automobiles")
		auto.save()
		health = Category(name="Health")
		health.save()
		pets = Category(name="Pets")
		pets.save()
		finance = Category(name="Finance")
		finance.save()
		cleaning = Category(name="Cleaning")
		cleaning.save()
		# Child categories
		modifications = Category(name="Modifications", parent=auto)
		modifications.save()
		maintenance = Category(name="Maintenance", parent=auto)
		maintenance.save()
		chiropractic = Category(name="Chiropractic", parent=health)
		chiropractic.save()
		petGrooming = Category(name="Grooming", parent=pets)
		petGrooming.save()
		petSitting = Category(name="Pet Sitting", parent=pets)
		petSitting.save()
		accounting = Category(name="Accounting", parent=finance)
		accounting.save()
		investing = Category(name="Investing", parent=finance)
		investing.save()
		homeCleaning = Category(name="Home", parent=cleaning)
		homeCleaning.save()
		officeCleaning = Category(name="Office", parent=cleaning)
		officeCleaning.save()
