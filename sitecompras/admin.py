from django.contrib import admin
from .models import Produtos, Cart, CartItem, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Produtos)
# Register your models here.
