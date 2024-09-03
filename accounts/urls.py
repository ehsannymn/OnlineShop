from django.urls import path, re_path
from accounts import views

urlpatterns = [
    path('registerUser', views.register_user, name='registerUser'),
    # path('registerRestaurant', views.register_restaurant, name='registerRestaurant'),
]
