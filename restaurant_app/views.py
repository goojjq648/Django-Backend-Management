from django.shortcuts import render

# Create your views here.
def restaurant_mainPage(request):
    return render(request, 'restaurant_app/restaurant_mainPage.html')