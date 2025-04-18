from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Restaurant
from .documents import RestaurantDocument

@receiver(post_save, sender=Restaurant)
def update_restaurant_index(sender, instance, **kwargs):
    RestaurantDocument().update(instance)

@receiver(post_delete, sender=Restaurant)
def delete_restaurant_index(sender, instance, **kwargs):
    RestaurantDocument().delete(instance)
