from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# MIXING PROFILE AND USER INFO
class ProfileInline(admin.StackedInline):
    model = Profile

# EXTENDING USER MODEL 
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# UNREGISTER THE OLD FORMAT
admin.site.unregister(User)

# REGISTER THE NEW FORMAT
admin.site.register(User, UserAdmin)
