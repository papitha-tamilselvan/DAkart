from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='addcart'),
    path('dec_cart/<int:product_id>/', views.decrement_cartItem, name='decrement_cart_item')
       
] 
