from django.contrib import admin
from .models import (
    Profile,
    Location,
    Product,
    Order,
    Comment,
    Buyer,
    Supplier,
    Insurance,
    Guarantee,
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Guarantee)
admin.site.register(Buyer)
admin.site.register(Supplier)
admin.site.register(Insurance)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Comment)
