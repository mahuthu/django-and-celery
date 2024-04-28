from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('customer/<int:customer_id>/', views.customer_view, name='customer_detail'),

]