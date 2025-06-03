from django.shortcuts import render

# Create your views here.
from django.db.models import FloatField
from django.db.models.expressions import RawSQL

from rest_framework import viewsets
from restaurant_app.models import Restaurant
from api.serializers import RestaurantSerializer

from django.conf import settings
from Backend_Manager.elasticsearch_client import es
from sentence_transformers import SentenceTransformer

search_model = SentenceTransformer('all-MiniLM-L6-v2')
search_category_index = 'category_semantic'


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        """根據 Vue.js 傳來的查詢參數 (`location` 和 `category`) 篩選餐廳"""
        queryset = Restaurant.objects.all()
        location = self.request.query_params.get('location')  # 取得地點參數
        category = self.request.query_params.get('category')  # 取得餐廳類型參數

        latitude = self.request.query_params.get('lat')  # 取得緯度參數
        longitude = self.request.query_params.get('lng')  # 取得經度參數

        print(f'location: {location}')
        print(f'category: {category}')
        print(f'latitude: {latitude}')
        print(f'longitude: {longitude}')

        # 設定篩選餐廳的最大距離
        max_distance = 5000

        if latitude and longitude:
            # `ST_Distance_Sphere` 會計算餐廳與使用者之間的距離（單位：公尺）
            distance_sql = """
                ST_Distance_Sphere(
                    point(longitude, latitude),
                    point(%s, %s)
                )
            """
            queryset = queryset.annotate(
                distance=RawSQL(distance_sql, (longitude, latitude),
                                output_field=FloatField())
            ).filter(distance__lte=max_distance).order_by('distance')

        # 篩選餐廳類型
        if category:
            # 查詢向量
            query_vector = search_model.encode(category).tolist()

            # 搜尋 Elasticsearch
            search_result = es.search(
                index=search_category_index,
                body={
                    "knn": {
                        "field": "embedding",
                        "query_vector": query_vector,
                        "k": 3,
                        "num_candidates": 100
                    }
                },
            )

            category_ids = [hit['_source']['name']
                            for hit in search_result['hits']['hits']]

            print(f'category_ids: {category_ids}')

            queryset = queryset.filter(categories__name__in=category_ids)

        return queryset
