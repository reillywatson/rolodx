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

site.register(Professional, ProfessionalIndex)
