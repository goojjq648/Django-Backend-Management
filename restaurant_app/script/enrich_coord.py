from restaurant_app.models import Streets
import requests
from urllib.parse import quote
from decimal import Decimal

def enrich_coord():
    streets = Streets.objects.filter(latitude__isnull=True)

    for street in streets:
        full_address = f"{street.city}{street.district}{street.road}"
        encoded_address = quote(full_address)
        
        url = f"https://nominatim.openstreetmap.org/search?format=json&q=${encoded_address}"
        hearders = { "User-Agent" : "MyRestaurantApp/1.0 (goojjq648@gmail.com)" }

        try:
            res = requests.get(url, headers=hearders)
            data = res.json()

            if data:
                street.latitude = Decimal(data[0]['lat'])
                street.longitude = Decimal(data[0]['lon'])
                street.save()
        except Exception as e:
            print(f"查詢失敗: {full_address}, 原因: {e}")
            



