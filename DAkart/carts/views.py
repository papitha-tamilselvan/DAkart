
import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from store.models import Product
from carts.models import Cart, CartItem

# Create your views here.
def _cart_id(request):
    cart_session_key = request.session.session_key

    if not cart_session_key:
        cart_session_key = request.session.create()
        return cart_session_key

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    try:
        cart_item = CartItem.objects.get(product = product,cart= cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        ) 
        return HttpResponse("cart does not exist block")  
        exit()  
        
      
def cart(request):
    return render(request, 'cart.html')