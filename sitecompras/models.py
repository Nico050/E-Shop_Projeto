from django.db import models
from django.contrib.auth.models import User

class Produtos(models.Model):
    name = models.CharField(max_length = 120)
    description = models.TextField()
    price = models.DecimalField(decimal_places = 2, max_digits = 10000)
    photo = models.ImageField()

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    s_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    s_cep = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return f'Carrinho de {self.user.username}'
    
    def get_parcial_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total
    
    def get_grand_total(self):
        return self.get_parcial_price() + self.s_cost
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} no {self.cart}'

    def get_total_price(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    Pay_Pix = 'Pix'
    Pay_Card = 'Cartão'
    Pay_Choices = [(Pay_Pix, 'PIX'), (Pay_Card, 'CARTÃO')]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    ship_cost = models.DecimalField(max_digits=10, decimal_places=2)
    ship_cep = models.CharField(max_length=9, null=True, blank=True)
    payment = models.CharField(max_length=8, choices=Pay_Choices, default=Pay_Pix)
    status = models.CharField(max_length=50, default='Processing')

    def __str__(self):
        return f'Pedido {self.id} de {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    products = models.ForeignKey(Produtos, on_delete=models.SET_NULL, null= True)

    product_name = models.CharField(max_length=120)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} X {self.products.name} (Pedido #{self.order.id})'

    def get_total_price(self):
        return self.products.price * self.quantity


# Create your models here.
