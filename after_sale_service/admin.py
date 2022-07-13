from django.contrib import admin
from .models import Service, Product, Tag, Partner

# Register your models here.
admin.site.register(Tag)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(Partner)
