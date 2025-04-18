from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from restaurant_app.documents import StreetsDocument

class SearchAddressView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            print("start search")
            
            # 使用 Elasticsearch 查詢，並搜尋 address 字段
            results = StreetsDocument.search().query("multi_match", query=query, fields=['city', 'district', 'road']).highlight('city', 'district', 'road')[:30]
            # 準備返回的資料
            data = [
                {
                    "city": hit.city,
                    "district": hit.district,
                    "road": hit.road,
                }
                for hit in results
            ]
            
            print(data)
            return Response(data)

        return Response([])

# class SearchAddressView(APIView):
#     def get(self, request):
#         query = request.GET.get('query', '')
#         if query:
#             print("start search")
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT city, district, road
#                     FROM streets
#                     WHERE city LIKE %s OR 
#                         district LIKE %s OR 
#                         road LIKE %s
#                     LIMIT 15
#                 """, [
#                     f"%{query}%", f"%{query}%", f"%{query}%"
#                 ])
#                 results = cursor.fetchall()

#             data = [
#                 {
#                     "city": row[0],
#                     "district": row[1],
#                     "road": row[2],
#                 }
#                 for row in results
#             ]

#             print(data)
#             return Response(data)

#         return Response([])
