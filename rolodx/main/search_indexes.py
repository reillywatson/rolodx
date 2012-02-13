from haystack import indexes
from main.models import Professional, Category, Service

# Adds category's name and all parents names to a list of category name strings
def categoryListRecursive(category):
	categories = [category.name]
	if category.parent is not None:
		categories.extend(categoryListRecursive(category.parent))
	return categories

class ProfessionalIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	location = indexes.LocationField(model_attr='get_location', null=True)
	averageRating = indexes.DecimalField(model_attr='averageRating', null=True)

	def get_model(self):
		return Professional
	def prepare(self, obj):
		self.prepared_data = super(ProfessionalIndex, self).prepare(obj)
		# Append each category name to field 'text'
		categoryList = []
		for category in obj.categories.all():
			categoryList.extend(categoryListRecursive(category))
		categoryList = set(categoryList)

		for cat in categoryList:
			self.prepared_data['text'] += ' %s' % cat
		return self.prepared_data
