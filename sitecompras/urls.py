from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produto_page/<produto_id>/', views.produto_page, name='produto_page'),
    path('cart/add/<produto_id>/', views.add_cart, name='add_cart'),
    path('cart/', views.cart_details, name='cart_details'),
    path('cart/remove/<item_id>/', views.remove_cart, name='remove_cart'),
    path('cart/update/<item_id>/', views.update_cart, name='update_cart'),
    path('cart/calculated_shipping/', views.calculate_shipping, name='calculated_shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process, name='process'),
    path('checkout/success/<order_id>/', views.success, name='success'),
]