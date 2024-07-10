from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# REGISTERING THE MODEL ON THE ADMIN SECTION
admin.site.register(ShippingAddress)
admin.site.register(Order) 
admin.site.register(OrderItem)

# CREATING AN ORDERITEM INLINE
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# EXTEND OUR ORDER MODEL
class OrderAdmin(admin.ModelAdmin):
    model = Order
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped"]
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

# UNREGISTERING ORDER MODEL
admin.site.unregister(Order)

# RE-REGISTERING OUR ORDER AND ORDERADMIN
admin.site.register(Order, OrderAdmin)


