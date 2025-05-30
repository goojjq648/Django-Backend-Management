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
    # 加入三個補字欄位：城市、區、路
    suggest_city = fields.CompletionField()
    suggest_district = fields.CompletionField()
    suggest_road = fields.CompletionField()
    suggest_full_address = fields.CompletionField()
    
    class Index:
        name = 'streets'

    class Django:
        model = Streets
        fields = ['city', 'district', 'road']
    
    def prepare_suggest_city(self, instance):
        city = instance.city.strip()
        variants = set()

        variants.add(city)

        # 臺 → 台
        if "臺" in city:
            city_alt = city.replace("臺", "台")
            variants.add(city_alt)

        # 去掉尾部「市」
        for c in list(variants):
            if c.endswith("市"):
                variants.add(c[:-1])  # 臺北市 → 臺北 / 台北市 → 台北

        return {
            "input": list(variants)
        }
    
    def prepare_suggest_district(self, instance):
        # 去除 city（如「臺北市士林區」→「士林區」）
        district = instance.district.replace(instance.city, "") if instance.city in instance.district else instance.district
        return {
            "input": [district]
        }
    
    def prepare_suggest_road(self, instance):
        return {
            "input": [instance.road]
        }

    def prepare_suggest_full_address(self, instance):
        city = instance.city.strip()
        raw_district = instance.district.strip()
        district = raw_district.replace(city, "") if city in raw_district else raw_district
        road = instance.road.strip()

        variants = set()

        # 單獨欄位
        variants.add(city)
        variants.add(district)
        variants.add(road)

        # 合併組合詞
        variants.add(f"{city}{district}{road}")
        variants.add(f"{district}{road}")
        variants.add(f"{city}{road}")
        variants.add(f"{city}{district}")

        # 異體字處理
        if "臺" in city:
            city_alt = city.replace("臺", "台")
            variants.add(f"{city_alt}{district}{road}")
            variants.add(f"{city_alt}{road}")
            variants.add(f"{district}{road}")
            variants.add(f"{city_alt}{district}")
            variants.add(city_alt)

        return {
            "input": list(variants)
        }

    class Meta:
        mappings = {
            'properties': {
                'city': {'type': 'keyword'},
                'district': {'type': 'keyword'},
                'road': {'type': 'keyword'}
            }
        }
