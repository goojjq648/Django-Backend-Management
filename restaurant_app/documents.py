from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Restaurant, Category, Restaurantcategory, Streets


@registry.register_document
class RestaurantDocument(Document):
    categories = fields.TextField(attr='get_categories')  

    class Index:
        name = 'restaurants'

    class Django:
        model = Restaurant
        fields = ['name', 'address']  

    def get_categories(self, obj):
        categories = Restaurantcategory.objects.filter(restaurant=obj)
        return [category.category.name for category in categories] if categories.exists() else []
    

@registry.register_document
class StreetsDocument(Document):
    class Index:
        name = 'streets'

    class Django:
        model = Streets
        fields = ['city', 'district', 'road']

    class Meta:
        mappings = {
            'properties': {
                'city': {'type': 'keyword'},
                'district': {'type': 'keyword'},
                'road': {'type': 'keyword'}
            }
        }
