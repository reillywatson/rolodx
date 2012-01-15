from rolodx.main.models import Professional, Category


class TestDataPopulator:
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

	def populate_test_professionals(self):
		josh = Professional(
			name="Josh JaySome Sumali",
			occupation="Coder Ninja",
			description="The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of darkness, for he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who would attempt to poison and destroy My brothers. And you will know My name is the Lord when I lay My vengeance upon thee.",
			email="j.sumali@gmail.com",
			website="https://github.com/jsumali",
			averageRating = 5,
			numRatings = 1)
		josh.save()

		josh2 = Professional(
			name="Josh2",
			occupation="Dev",
			description="Bacon ipsum dolor sit amet tri-tip corned beef venison rump, short ribs short loin turducken brisket cow shoulder capicola filet mignon spare ribs pork chop salami. Jowl shankle frankfurter, spare ribs boudin brisket rump andouille pancetta venison pastrami. Cow tail shoulder, sausage andouille salami fatback filet mignon tri-tip boudin beef ribs t-bone. Shankle t-bone sausage pork turkey rump. Frankfurter chicken pig, filet mignon shoulder brisket biltong pork meatloaf ham hock short ribs jerky pastrami pork chop shank. Short loin t-bone filet mignon, flank prosciutto ground round cow. Ham pancetta strip steak salami, pork belly shankle tail short ribs ball tip capicola filet mignon sirloin.",
			email="j.sumali@gmail.com",
			website="https://github.com/jsumali",
			averageRating = 5,
			numRatings = 1)
		josh2.save()

		josh3 = Professional(
			name="Josh JaySome Sumali",
			occupation="Bacon",
			description="Bacon ipsum dolor sit amet pig ham hock leberkase, pork chop meatloaf bacon short ribs sirloin biltong chicken. Turkey tri-tip cow, beef ribs pastrami swine strip steak salami bacon jowl. Pork pig ribeye corned beef tenderloin prosciutto. Chuck flank biltong rump, shank prosciutto turducken t-bone pork chop ham leberkase. Ribeye sirloin jowl, turducken venison prosciutto fatback biltong short loin salami t-bone meatball tail. Short loin tri-tip pork, leberkase beef ribs t-bone ground round shankle. Cow prosciutto jerky, biltong fatback turkey tail.",
			email="j.sumali@gmail.com",
			website="https://github.com/jsumali",
			averageRating = 5,
			numRatings = 1)
		josh3.save()

		reilly = Professional(
			name="Reilly Rilester Watson",
			occupation="Chief Developer Officer",
			description="Lorizzle ipsizzle dolor uhuh ... yih! amizzle, consectetizzle adipiscing elit. Its fo rizzle get down get down dang, aliquet we gonna chung, owned quis, gravida vizzle, fizzle. Pellentesque egizzle tortizzle. Sizzle erizzle. Sure izzle dolizzle dapibus turpizzle yo mamma crackalackin. Maurizzle dang shizzle my nizzle crocodizzle ghetto turpizzle. Check it out izzle tortor. Pellentesque eleifend rhoncizzle da bomb. In hizzle sure platea dictumst. Da bomb dapibus. Curabitur tellizzle i'm in the shizzle, pretizzle fo shizzle, mattizzle gangsta, eleifend vitae, nunc. Doggy suscipit. Shizzlin dizzle da bomb velit own yo' dawg.",
			email="reillywatson@gmail.com",
			website="https://github.com/reillywatson",
			averageRating = 5,
			numRatings = 1)
		reilly.save()

		helen = Professional(
			name="Helen DotDotDot Huo",
			occupation="Le Artiste",
			description="Cupcake ipsum dolor. Sit amet powder. Carrot cake candy faworki donut topping icing sweet applicake bonbon. Tiramisu chocolate bar wafer liquorice sesame snaps ice cream candy canes ice cream. Gummi bears sugar plum cake. Oat cake candy liquorice cake pudding. Pie souffle pastry cake sweet roll cotton candy. Sweet roll pastry bonbon. Sesame snaps donut faworki apple pie muffin danish sweet faworki tart. Ice cream muffin jelly-o chocolate bar marzipan. Brownie liquorice icing tootsie roll cotton candy ice cream chocolate danish. Chocolate cake candy icing lemon drops tiramisu lollipop.",
			email="hhuo.hj@gmail.com",
			website="https://github.com",
			averageRating=5,
			numRatings=1
		)
		helen.save()

