from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # GETTING THE CART
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    # GET THE CART
    cart = Cart(request)
    # TEST FOR POST
    if request.POST.get('action') == 'post':
        # GETTING STUFF
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        # LOOKUP PRODUCT IN THE DB
        product = get_object_or_404(Product, id = product_id)
        
        # SAVE TO SESSION
        cart.add(product=product, quantity=product_qty)
        
        # GET CART QUANTITY
        cart_quantity = cart.__len__()
        
        # RETURN RESPONSE
        # response = JsonResponse({'Product Name: ': product.name })
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response
        
def cart_delete(request):
    cart = Cart(request)
    # TEST FOR POST
    if request.POST.get('action') == 'post':
    # GETTTING STUFF
        product_id = int(request.POST.get('product_id'))
        # CALLING DELETE FUNCTION IN CART
        cart.delete(product=product_id)
        
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Product Has Been Deleted From Your Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    # TEST FOR POST
    if request.POST.get('action') == 'post':
    # GETTTING STUFF
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
    # UPDATING THE CART
        cart.update(product=product_id, quantity=product_qty)
    
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Your Cart Has Been Successfully Updated..."))
        return response
    