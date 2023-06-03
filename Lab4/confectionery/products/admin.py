from django.contrib import admin

from products.models import Product, Category, Manufacturer

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Manufacturer)

