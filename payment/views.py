from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # GETTING THE ORDER
        order = Order.objects.get(id=pk)
        # GETTING THE ORDER ITEMS
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # CHECKING IF STATUS IS TRUE OR FALSE
            if status == "true":
                # GETTING THE ORDER
                order = Order.objects.filter(id=pk)
                # UPDATING THE STATUS
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # GETTING THE ORDER
                order = Order.objects.filter(id=pk)
                # UPDATING THE STATUS
                order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')

        return render(request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied!!!")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False) 
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # GETTING THE ORDER
            order = Order.objects.filter(id=num)
            # GRABBING DATE AND TIME
            now = datetime.datetime.now()
            # UPDATING ORDER
            order.update(shipped=True, date_shipped=now)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')
        
        return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, "Access Denied!!!")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True) 
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # GETTING THE ORDER
            order = Order.objects.filter(id=num)
            # GRABBING DATE AND TIME
            now = datetime.datetime.now()
            # UPDATING ORDER
            order.update(shipped=False, date_shipped = now)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')
        
        return render(request, 'payment/shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, "Access Denied!!!")
        return redirect('home')

def process_order(request):
    if request.POST:
        # GETTING THE CART
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # GETTING BILLING INFO FROM THE LAST PAGE
        payment_form = PaymentForm(request.POST or None)
        # GETTING SHIPPING SESSION DATA
        my_shipping = request.session.get('my_shipping')
       
        # GATHERING ORDER INFO
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # CREATING A SHIPPING ADDRESS FROM SESSION INFO 
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}" 
        amount_paid = totals

        # CREATING AN ORDER
        if request.user.is_authenticated:
            # IF USER IS LOGGED IN 
            user = request.user 
            # CREATING ORDER
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # ADDING ORDER ITEMS 

            # GETTING THE ORDER ID
            order_id = create_order.pk

            # GETTING PRODUCT INFO
            for product in cart_products():
                # GETTING PRODUCT ID
                product_id = product.id
                # GETTING PRODUCT PRICE
                if product.for_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # GETTING QUANTITY
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # CREATING ORDER ITEM
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # DELETING OUR CART AFTER PROCESSING ORDER
            for key in list(request.session.keys()):
                if key == "session_key":
                    # DELETING KEY
                    del request.session[key]
                
            # DELETNG CART FROM DATABASE(OLD CART FIELD)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # DELETNG CART FROM DATABASE(OLD CART FIELD)
            current_user.update(old_cart="")    

            messages.success(request, "Order Placed")
            return redirect('home')
        else:   
            # IF USER IS NOT LOGGED IN 
            # CREATING AN ORDER
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # DELETING OUR CART AFTER PROCESSING ORDER
            for key in list(request.session.keys()):
                if key == "session_key":
                    # DELETING KEY
                    del request.session[key]
            messages.success(request, "Order Placed!!!")
            return redirect('home')
    else:
        messages.success(request, "Access Denied!!!")
        return redirect('home')

def billing_info(request):
    if request.POST:   
        # GETTING THE CART
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # CREATING A SESSION WITH THE SHIPPING INFO 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
         

        # CHECKING TO SEE IF USER IS LOGGED IN 
        if request.user.is_authenticated:
            # GETTING THE BILLING FORM
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        # CHECKING TO SEE IF USER IS NOT LOGGED IN 
        else:
            # GETTING THE BILLING FORM
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied!!!")
        return redirect('home')
    
def checkout(request):
    # GETTING THE CART
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # CHECKOUT AS LOGGED IN USER
        # SHIPPING USER
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # SHIPPING FORM 
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # CHECKOUT AS GUEST
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

def payment_success(request):
    return render(request, "payment/payment_success.html", {})
