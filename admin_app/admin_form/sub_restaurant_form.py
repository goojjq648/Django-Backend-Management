from django import forms
from restaurant_app.models import Restaurant
from .BaseModelLabelForm import BaseModelLabelForm



class RestaurantForm(BaseModelLabelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'hash_value', 'rating', 'review_count', 'address', 'phone_number',
                  'average_spending', 'opening_hours', 'services', 'latitude',
                  'longitude', 'image_url', 'google_url']
    
        widgets = {
            'name': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantName', 'class': 'form-control', 'name': 'restaurant_name','data-alert': 'true'}
                ),
            'hash_value': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantHash', 'class': 'form-control', 'name': 'restaurant_hash_value','readonly': 'true'}
                ),
            'rating': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantRating', 'class': 'form-control', 'name': 'restaurant_rating','data-alert': 'true'}
                ),
            'review_count': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantReviewCount', 'class': 'form-control', 'name': 'restaurant_review_count'}
                   ),
            'address': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantAddress', 'class': 'form-control', 'name': 'restaurant_address'}
                   ),
            'phone_number': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantPhone', 'class': 'form-control', 'name': 'restaurant_phone_number'}
                    ),
            'average_spending': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantAverageSpending', 'class': 'form-control', 'name': 'restaurant_average_spending'}
                    ),
            'opening_hours': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantBusinessHours', 'class': 'form-control', 'name': 'restaurant_business_hours','data-alert': 'true'}
                   ),
            'services': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantServices', 'class': 'form-control', 'name': 'restaurant_services','data-alert': 'true'}
                   ),
            'latitude': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantLatitude', 'class': 'form-control', 'name': 'restaurant_latitude','data-alert': 'true'}
                   ),
            'longitude': 
                forms.TextInput(
                    attrs={'id': 'InputRestaurantLongitude', 'class': 'form-control', 'name': 'restaurant_longitude','data-alert': 'true'}
                    ),
            'image_url': 
                forms.TextInput(
                   attrs={'id': 'InputRestaurantImageUrl', 'class': 'form-control', 'name': 'restaurant_image_url'}
                   ),
            'google_url': 
                forms.URLInput(
                   attrs={'id': 'InputRestaurantGoogleUrl', 'class': 'form-control', 'name': 'restaurant_google_url'}
                   )
        }
