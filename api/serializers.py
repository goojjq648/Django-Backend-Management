from django.conf import settings
import os
from rest_framework import serializers
from restaurant_app.models import Restaurant, Category, Restaurantcategory, Businesshours, Restaurantimage

# 餐廳分類序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # 只顯示分類 ID & 名稱

# 餐廳營業時間序列化器
class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Businesshours
        fields = ['day_of_week', 'open_time', 'close_time']  # 顯示營業時間資訊

#  餐廳圖片序列化器
class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurantimage
        fields = ['image_url']  # 只顯示圖片網址

# 餐廳主序列化器（包含分類、營業時間、圖片）
class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  # 讀取時顯示分類名稱
    business_hours = BusinessHoursSerializer(many=True, read_only=True, source='businesshours_set')  # 讀取時顯示營業時間
    images = RestaurantImageSerializer(many=True, read_only=True, source='restaurantimage_set')  # 讀取時顯示餐廳圖片

    # 允許前端用分類 ID 建立關聯
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='categories',  # 這樣寫入時 API 會知道對應的是 `categories`
        many=True
    )

    # 新增 `image_url` 欄位（補上完整路徑）
    real_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'  # 讓 API 顯示所有欄位，包括關聯資訊

    def get_real_image_url(self, obj):
        """ 透過 `image` 欄位補上完整的圖片 URL """
        if obj.image_url:  # 確保 `image` 欄位不為空
            image_path = os.path.join(settings.STATIC_URL, "images/restaurant_app/", obj.image_url)

                    # 若在開發環境，直接使用 request.build_absolute_uri
            request = self.context.get("request")
            if request and settings.DEBUG:
                return request.build_absolute_uri(image_path)
            
            return image_path
        
        return None