import os
from django.conf import settings

# 定義抓取爬蟲資料的資料夾路徑
def getRestaurantScraperDataFolder():
    return os.path.join(settings.BASE_DIR, 'restaurant_app', 'static', 'restaurant_data')
