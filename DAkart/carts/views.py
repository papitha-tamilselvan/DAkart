
import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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
        if cart_item.is_active ==0:
            cart_item.is_active = 1
            cart_item.save()
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        ) 

    return redirect ('cart')   

def decrement_cartItem(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)  
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save() 
    else:
        cart_item.is_active=0
        cart_item.quantity=0
        cart_item.save()

    return redirect('cart')  

def cart(request, total = 0, quantity = 1, cart_items = None):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_items = CartItem.objects.filter(cart= cart, is_active = True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)

    context = {
        'cartItems':cart_items,
        'total':total

    }    

    return render(request, 'cart.html', context)