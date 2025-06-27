# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import hashlib
from django.utils.dateparse import parse_time
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'category'


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='編號')
    name = models.CharField(max_length=255, verbose_name='餐廳名稱')
    hash_value = models.CharField(max_length=64, unique=True, blank=False, null=False, verbose_name='Hash 值')
    rating = models.FloatField(verbose_name='評分')
    review_count = models.IntegerField(verbose_name='評論數', default=0)
    address = models.CharField(max_length=255, verbose_name='地址', blank=False, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='電話號碼')  # 新增電話號碼欄位
    average_spending = models.CharField(max_length=255, blank=True, null=True, verbose_name='平均消費')
    opening_hours = models.JSONField(blank=True, null=True, verbose_name='營業時間')
    services = models.JSONField(blank=True, null=True, verbose_name='提供服務')
    latitude = models.FloatField(verbose_name='緯度', blank=False, null=False)
    longitude = models.FloatField(verbose_name='經度', blank=False, null=False)
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='圖片網址')
    google_url = models.URLField(max_length=1000, null=True, blank=True, verbose_name='google網址')  # Google Maps 連結欄位
    # 其他欄位
    categories = models.ManyToManyField(Category, through='Restaurantcategory')

    def as_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}
    

    def save(self, *args, **kwargs):
        if not self.hash_value:
            self.hash_value = self.generateHash()

        super(Restaurant, self).save(*args, **kwargs)

        # 更新餐廳的 Businesshours
        self.updateBusinesshours()

    def generateHash(self):
        combined_string = f"{self.name}{self.address}"
        return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()
    
    def generateHashValue(name, address):
        if not name or not address:
            return None
        
        combined_string = f"{name}{address}"
        return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()
        
    
    def updateBusinesshours(self):
        if not self.opening_hours:
            return
        
        # 刪除當前餐廳的所有 Businesshours 以避免重複
        Businesshours.objects.filter(restaurant=self).delete()

        # 確保 opening_hours 有數據
        if self.opening_hours:
            for day, bussinesstime in self.opening_hours.items():
                open_time, close_time = self.parseBusinesshours(bussinesstime)

                if open_time is None or close_time is None:
                    continue
                
                Businesshours.objects.create(
                    restaurant=self,
                    day_of_week=day,
                    open_time=open_time,
                    close_time=close_time
                )

    def parseBusinesshours(self, timedata):
        try:
            if not timedata or timedata.strip() in ["休息", ""] or '到' not in timedata:
                return None, None
        
            # sample : "星期日": "10:30 到 13:50"
            open_time_str, close_time_str = timedata.split(' 到 ')
            open_time = datetime.strptime(open_time_str, "%H:%M").time()
            close_time = datetime.strptime(close_time_str, "%H:%M").time()
            return open_time, close_time
        except Exception as e:
            return None, None
    
    
    def updateCategoriesFromJson(self, json_data):
        # 假設 json_data 包含 'categories' 字段，格式類似 ['燒肉', '壽司']
        category_names = json_data.get('categories', [])

        # 清除現有的類型關聯
        self.categories.clear()

        # 添加新的類型
        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            self.categories.add(category)

    def addCategories(self, type):
        category, created = Category.objects.get_or_create(name=type)
        self.categories.add(category)


    class Meta:
        managed = False
        db_table = 'restaurant'

class Businesshours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'businesshours'


class Restaurantcategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE)
    # The composite primary key (restaurant_id, category_id) found, that is not supported. The first column is selected.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'restaurantcategory'
        unique_together = (('restaurant', 'category'))

    


class Restaurantimage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'restaurantimage'


class Streets(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    road = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'streets'
        unique_together = (('city', 'district', 'road'),)


class Restaurantreview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'RestaurantReview'
        unique_together = (('user', 'restaurant'),)


class Restaurantfavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'RestaurantFavorite'
        unique_together = (('user', 'restaurant'),)
