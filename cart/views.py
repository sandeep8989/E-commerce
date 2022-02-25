from typing import Counter
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            item = CartItem.objects.get(product=product)
            item.quantity += 1
            item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(
                product = product,
                quantity = 1,
                cart=cart,
            )
            cart_item.save()
        
        return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):

    global context

    try:
        #tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        #tax = (2 * total)/100
        grand_total = total 
        
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        #'tax'       : tax,
        'grand_total': grand_total,
    }

    return render(request, "cart/shop_wishlist.html", context)


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id= product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def shop_checkout(request, total=0, quantity=0, cart_items=None):

    try:
        #tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        #tax = (2 * total)/100
        grand_total = total 
        
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, "cart/shop_checkout.html", context)