from django.shortcuts import render
from django.conf import settings

from django.db.models import FloatField
from django.db.models.expressions import RawSQL

from rest_framework import viewsets, serializers, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from restaurant_app.models import Restaurant, Restaurantreview, Restaurantfavorite

from api.serializers import RestaurantSerializer, RestaurantReviewSerializer, RestaurantFavoriteSerializer

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


class RestaurantReviewViewSet(viewsets.ModelViewSet):
    queryset = Restaurantreview.objects.all()
    serializer_class = RestaurantReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        else:
            return []

    def get_queryset(self):
        query = self.queryset
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            query = query.filter(restaurant_id=restaurant_id)
            return query
        else:
            query = self.queryset.none()

        return query

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response([], status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"驗證失敗{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({'error': f":{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("你沒有權限修改這筆資料。")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("你沒有權限刪除這筆資料。")
        instance.delete()


class RestaurantFavoriteViewSet(viewsets.ModelViewSet):
    queryset = Restaurantfavorite.objects.all()
    serializer_class = RestaurantFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("你沒有權限刪除這筆收藏。")
        instance.delete()
