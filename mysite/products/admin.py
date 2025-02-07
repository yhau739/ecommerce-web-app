from django.contrib import admin

# Register your models here.
# Make apps modifiable on admin

from .models import Product, Category, Order, OrderItem, Rating, ProductLike

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(ProductLike)