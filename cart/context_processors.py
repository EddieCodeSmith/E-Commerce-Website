from .cart import Cart

# CREATING CONTEXT PROCESSORS SO THAT OUR CART CAN WORK ON ALL PAGES OF THE SITE 
def cart(request):
    # RETURNING THE DEFAULT DATA FROM OUR CART
    return {'cart': Cart(request)}