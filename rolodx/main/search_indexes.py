from haystack.indexes import *
from haystack import site
from main.models import Professional, Category, Service
import decimal

# NOTE: Haystack doesn't currently recognize the tdouble field in the schemas
# it generates, and we're using it for lat/long data.
# So if you're modifying this, you may need to edit schema.xml by hand.
class ProfessionalIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	address_latitude = DecimalField(model_attr='address_latitude', null=True)
	address_longitude = DecimalField(model_attr='address_longitude', null=True)

	def prepare(self, object):
		self.prepared_data = super(ProfessionalIndex, self).prepare(object)

		# Append each category name to field 'text'
		for category in object.categories.all():
			if category is not None and category.name is not None:
				self.prepared_data['text'] += ' %s' % category.name

		return self.prepared_data

site.register(Professional, ProfessionalIndex)
