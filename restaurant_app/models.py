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

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'category'


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    hash_value = models.CharField(max_length=64, unique=True, blank=False, null=False)
    rating = models.FloatField()
    review_count = models.IntegerField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # 新增電話號碼欄位
    average_spending = models.CharField(max_length=255, blank=True, null=True)
    opening_hours = models.JSONField(blank=True, null=True)
    services = models.JSONField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_url = models.CharField(max_length=500, blank=True, null=True)
    google_url = models.URLField(max_length=1000, null=True, blank=True)  # Google Maps 連結欄位
    # 其他欄位
    categories = models.ManyToManyField(Category, through='Restaurantcategory')
    

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
        # 刪除當前餐廳的所有 Businesshours 以避免重複
        Businesshours.objects.filter(restaurant=self).delete()

        # 確保 opening_hours 有數據
        if self.opening_hours:
            for day, bussinesstime in self.opening_hours.items():
                open_time, close_time = self.parseBusinesshours(bussinesstime)

                Businesshours.objects.create(
                    restaurant=self,
                    day_of_week=day,
                    open_time=open_time,
                    close_time=close_time
                )

    def parseBusinesshours(self, timedata):
        # sample : "星期日": "10:30 到 13:50"
        open_time_str, close_time_str = timedata.split(' 到 ')
        open_time = datetime.strptime(open_time_str, "%H:%M").time()
        close_time = datetime.strptime(close_time_str, "%H:%M").time()
        return open_time, close_time
    
    
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
