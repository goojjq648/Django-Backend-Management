from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Restaurant, Category
from .documents import RestaurantDocument
from Backend_Manager.elasticsearch_client import es
from sentence_transformers import SentenceTransformer

@receiver(post_save, sender=Restaurant)
def update_restaurant_index(sender, instance, **kwargs):
    RestaurantDocument().update(instance)

@receiver(post_delete, sender=Restaurant)
def delete_restaurant_index(sender, instance, **kwargs):
    RestaurantDocument().delete(instance)

@receiver(post_save, sender=Category)
def index_categories(sender, instance, created, **kwargs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # 若為TRUE是新增的類別 不是就是更新
    if created:
        embedding = model.encode(instance.name).tolist()
        es.index(index="category_semantic", body={
            "name": instance.name,
            "embedding": embedding
        })
