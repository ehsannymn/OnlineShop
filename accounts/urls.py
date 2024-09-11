from django.urls import path, re_path
from accounts import views

urlpatterns = [
    path('registerUser', views.register_user, name='registerUser'),
    path('registerVendor', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.my_account, name='myAccount'),

    path('customerDashboard/', views.customer_dashboard, name='customerDashboard'),
    path('vendorDashboard/', views.vendor_dashboard, name='vendorDashboard'),


]
