from haystack import indexes
from main.models import Professional, Category, Service

# Adds category's name and all parents names to a list of category name strings
def PopulateCategoryListRecursive(category, categoryList):
	if category.name not in categoryList:
		categoryList.append(category.name)
	if category.parent is not None:
		PopulateCategoryListRecursive(category.parent, categoryList)

# NOTE: Haystack doesn't currently recognize the tdouble field in the schemas
# it generates, and we're using it for lat/long data.
# So if you're modifying this, you may need to edit schema.xml by hand.
class ProfessionalIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	address_latitude = indexes.DecimalField(model_attr='address_latitude', null=True)
	address_longitude = indexes.DecimalField(model_attr='address_longitude', null=True)

	def get_model(self):
		return Professional
	def prepare(self, object):
		self.prepared_data = super(ProfessionalIndex, self).prepare(object)

		# Append each category name to field 'text'
		categoryList = []
		for category in object.categories.all():
			PopulateCategoryListRecursive(category, categoryList)

		for cat in categoryList:
			self.prepared_data['text'] += ' %s' % cat

		return self.prepared_data
