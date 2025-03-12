from django.shortcuts import render

# Create your views here.
from django.db.models import FloatField
from django.db.models.expressions import RawSQL

from rest_framework import viewsets
from restaurant_app.models import Restaurant
from .serializers import RestaurantSerializer

from django.conf import settings


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

        max_distance = 5000

        # if category:
        #     queryset = queryset.filter(categories__name=category)
        #     print(queryset.query)

        if latitude and longitude:
            # `ST_Distance_Sphere` 會計算餐廳與使用者之間的距離（單位：公尺）
            distance_sql = """
                ST_Distance_Sphere(
                    point(longitude, latitude),
                    point(%s, %s)
                )
            """
            queryset = queryset.annotate(
                distance=RawSQL(distance_sql, (longitude, latitude), output_field=FloatField())
            ).filter(distance__lte=max_distance).order_by('distance')


        return queryset
