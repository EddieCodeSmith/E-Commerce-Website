from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # GETTING THE REQUEST   
        self.request = request
        # GETTING THE SESSION KEY IF IT EXISTS
        cart = self.session.get('session_key')
        
        # IF USER IS NEW, THEN THERE WILL BE NO SESSION KEY
        # CREATE ONE!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # MAKING SURE CART IS AVAILABLE ON ALL PAGES OF THE SITE 
        self.cart = cart
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # LOGIC
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # DEALING WITH LOGGED IN USER
        if self.request.user.is_authenticated:
            # GETTING THE CURRENT USER PROFILE 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # CONVERTING {'3':1, '2':4} TO {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # SAVING CARTY TO THE PROFILE MODEL
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # LOGIC
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # DEALING WITH LOGGED IN USER
        if self.request.user.is_authenticated:
            # GETTING THE CURRENT USER PROFILE 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # CONVERTING {'3':1, '2':4} TO {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # SAVING CARTY TO THE PROFILE MODEL
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # GETTING PRODUCT IDS
        product_ids = self.cart.keys()
        # LOOKING UP THE KEYS IN OUR PRODUCTS DATABASE MODEL
        products = Product.objects.filter(id__in=product_ids)
        # GETTING QUANTITIES
        quantities = self.cart    
        # STARTING COUNT FROM 0
        total = 0
        for key, value in quantities.items():
            # CONVERTING KEY STRING INTO AN INTEGER SO WE CAN APPLY LOGIC
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.for_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # GETTING ID'S FROM THE CART
        product_ids = self.cart.keys()
        # USE ID'S TO LOOKUP PRODUCTS IN DATABASE MODEL
        products = Product.objects.filter(id__in=product_ids)
        # RETURNING THE LOOKED-UP PRODUCTS 
        return products 
        
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # GETTING CART
        mycart = self.cart
        # UPDATING CART/DICTIONARY
        mycart[product_id] = product_qty
        
        self.session.modified = True
        
        # DEALING WITH LOGGED IN USER
        if self.request.user.is_authenticated:
            # GETTING THE CURRENT USER PROFILE 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # CONVERTING {'3':1, '2':4} TO {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # SAVING CARTY TO THE PROFILE MODEL
            current_user.update(old_cart=str(carty))
            
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        # DELETING FROM CART/DICTIONARY
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True 

         # DEALING WITH LOGGED IN USER
        if self.request.user.is_authenticated:
            # GETTING THE CURRENT USER PROFILE 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # CONVERTING {'3':1, '2':4} TO {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # SAVING CARTY TO THE PROFILE MODEL
            current_user.update(old_cart=str(carty))