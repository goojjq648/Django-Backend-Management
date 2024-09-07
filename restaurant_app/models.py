# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'category'


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    review_count = models.IntegerField()
    address = models.CharField(max_length=255)
    average_spending = models.CharField(max_length=255, blank=True, null=True)
    opening_hours = models.JSONField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_url = models.CharField(max_length=500, blank=True, null=True)

    categories = models.ManyToManyField(Category, through='Restaurantcategory')

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
        unique_together = (('restaurant', 'category'),)


class Restaurantimage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'restaurantimage'
