from django.contrib import admin
from django.urls import path
from .views import *

app_name='items'

urlpatterns = [
    path('', home,name='home'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',logoutview,name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('products/',products,name='products'),
    path('workoutplans/',workoutplans,name='workoutplans'),
    path('cart/',cart,name='cart'),
    path('update_item/',updateitem,name='update_item'),
]