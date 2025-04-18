from django.apps import AppConfig

class RestaurantAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant_app'

    def ready(self):
        from . import scheduler
        print('restaurant_app ready')
        # scheduler.start()
