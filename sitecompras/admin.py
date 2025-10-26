from django.contrib import admin
from .models import Produtos, Cart, CartItem, Order, OrderItem, Reviews

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Produtos)
admin.site.register(Reviews)

# Register your models here.
