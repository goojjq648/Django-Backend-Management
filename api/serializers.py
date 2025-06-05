from django.conf import settings
import os
from rest_framework import serializers
from restaurant_app.models import Restaurant, Category, Restaurantcategory, Businesshours, Restaurantimage, Restaurantfavorite, Restaurantreview
from django.contrib.auth.models import User
from user.models import UserUserprofile
import uuid

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
    categories = CategorySerializer(many=True, read_only=True)   # 讀取時顯示分類名稱
    business_hours = BusinessHoursSerializer(
        many=True, read_only=True, source='businesshours_set')   # 讀取時顯示營業時間
    images = RestaurantImageSerializer(
        many=True, read_only=True, source='restaurantimage_set') # 讀取時顯示餐廳圖片

    # 新增或更新可以用id建立分類
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
            image_path = os.path.join(
                settings.STATIC_URL, "images/restaurant_app/", obj.image_url)

            # 若在開發環境，直接使用 request.build_absolute_uri
            request = self.context.get("request")
            if request and settings.DEBUG:
                return request.build_absolute_uri(image_path)

            return image_path

        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'username': {'required': False},
            'password': {'write_only': True},  # 密碼不能回傳
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email 已經被註冊了。")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("密碼長度至少 8 個字元。")
        return value

    def generate_uuid_username(self):
        return uuid.uuid4().hex[:8]
    
    def validate(self, attrs):
        if not attrs.get('username'):
            attrs['username'] = self.generate_uuid_username()
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUserprofileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserUserprofile
        fields = ['user', 'google_id', 'avatar_url', 'role']

    def create(self, validated_data):
        # 取出 user
        user_data = validated_data.pop('user')

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        return UserUserprofile.objects.create(user=user, **validated_data)


# 評論 
class RestaurantReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = Restaurantreview
        fields = ['id', 'user', 'restaurant_id', 'rating', 'review', 'created_at', 'updated_at', 'avatar_url', 'username']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'avatar_url', 'username']

    def get_username(self, obj):
        return obj.user.username

    def get_avatar_url(self, obj):
        if obj.user.useruserprofile.avatar_url:
            return obj.user.useruserprofile.avatar_url
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = Restaurant.objects.get(pk=self.context['request'].data['restaurant_id'])

        # 檢查是否已經評論過
        if Restaurantreview.objects.filter(user=user, restaurant_id=restaurant).exists():
            raise serializers.ValidationError("已經評論過了。")


        validated_data['user'] = self.context['request'].user
        validated_data['restaurant_id'] = self.context['request'].data['restaurant_id']
        return super().create(validated_data)


# 收藏
class RestaurantFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurantfavorite
        fields = ['id', 'user', 'restaurant', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
