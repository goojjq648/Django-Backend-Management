from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from restaurant_app.documents import StreetsDocument
from elasticsearch_dsl import Q

class SearchAddressView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        if not query:
            return Response([])
        
        search = StreetsDocument.search()
        # 同時發出三種補字查詢
        search = search.suggest(
            'city-suggest', query,
            completion={"field": "suggest_city", "fuzzy": {"fuzziness": 1}, "size": 5}
        ).suggest(
            'district-suggest', query,
            completion={"field": "suggest_district", "fuzzy": {"fuzziness": 1}, "size": 5}
        ).suggest(
            'road-suggest', query,
            completion={"field": "suggest_road", "fuzzy": {"fuzziness": 1}, "size": 5}
        ).suggest(
            'full-address-suggest', query,
            completion={"field": "suggest_full_address", "fuzzy": {"fuzziness": 1}, "size": 5}
        )

        response = search.execute()

        data = []
        for suggest_name in ['city-suggest', 'district-suggest', 'road-suggest', 'full-address-suggest']:
            if suggest_name in response.suggest:
                options = response.suggest[suggest_name][0].options
                print(f'options: {options}')  # 印出建議
                if options:
                    data = [
                        {
                            "city": opt._source.city,
                            "district": opt._source.district.replace(opt._source.city, ""),
                            "road": opt._source.road
                        }
                        for opt in options
                    ]
                    break  # 用第一個有結果的建議即可

        return Response(data)

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
