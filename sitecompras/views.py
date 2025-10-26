from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Produtos, Cart, CartItem, Order, OrderItem
from django.contrib import messages


# Create your views here.

def index(request):
    produto = Produtos.objects.all()
    context = {"produtos": produto}
    return render(request, 'sitecompras/index.html', context)

def produto_page(request, produto_id):
    produto = Produtos.objects.get(id=produto_id)
    context = {"produto": produto}
    return render(request, 'sitecompras/produto_page.html', context)

def reset_ship(cart):
    cart.s_cost = 0.00
    cart.s_cep = None
    cart.save()

@login_required
def add_cart(request, produto_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    produto = get_object_or_404(Produtos, id=produto_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product = produto, defaults={'quantity': quantity})
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    reset_ship(cart)

    return redirect('index')

@login_required
def cart_details(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'sitecompras/cart_details.html', context)

@login_required
def remove_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    cart_do_item = cart_item.cart
    reset_ship(cart_do_item)
    cart_item.delete()
    return redirect('cart_details')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user = request.user)

    reset_ship(cart_item.cart)

    try:
        new_quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, 'A quantidade deve ser um número válido.')
        return redirect('cart_details')

    if new_quantity <= 0:
        messages.error(request, 'A quantidade deve ser maior que zero.')
        return redirect('cart_details')
    elif new_quantity > 999:
        messages.error(request, 'A quantidade não pode ser maior que 999.')
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'A quantidade do produto "{cart_item.product.name}" foi atualizada para {new_quantity}.')
    return redirect('cart_details')

@login_required
def calculate_shipping(request):
    cart=get_object_or_404(Cart, user=request.user)
    cep = request.POST.get('cep', '').strip().replace('-', '')

    if not cep or len(cep) != 8 or not cep.isdigit():
        messages.error(request, 'Por favor, informe um CEP válido.')
        return redirect('cart_details')
    calculate_shipping = 0.00
    subtotal = cart.get_parcial_price()
    if subtotal > 200:
        calculate_shipping = 0.00
        messages.success(request, 'Frete Grátis aplicado!')
    else:
        calculate_shipping = 15.00
        messages.success(request, f'Frete de R$15,00 aplicado para o CEP: {cep}')
    cart.s_cost = calculate_shipping
    cart.s_cep = cep
    cart.save()

    return redirect('cart_details')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.all().exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('cart_details')
    if cart.s_cep is None:
        messages.error(request, 'Por favor, calcule o frete antes de prosseguir.')
        return redirect('cart_details')
    payment_choices = Order.Pay_Choices
    context = {'cart': cart, 'payment_choices': payment_choices}
    return render(request, 'sitecompras/checkout.html', context)

@login_required
def process(request):
    print("Processando pedido...")
    cart = get_object_or_404(Cart, user=request.user)
    payment_method = request.POST.get('payment_method')
    valid_choices = [choice[0] for choice in Order.Pay_Choices]

    if payment_method not in valid_choices:
        messages.error(request, 'Por favor, selecione um método de pagamento válido.')
        return redirect('checkout')
    
    if not cart.items.all().exists() or cart.s_cep is None:
        messages.error(request, 'Seu carrinho está vazio ou o frete não foi calculado.')
        return redirect('cart_details')
    
    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_paid=cart.get_grand_total(),
                ship_cost=cart.s_cost,
                ship_cep=cart.s_cep,
                payment=payment_method,
                status='Paid',
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    products=item.product,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity
                )
            
            cart.items.all().delete()
            reset_ship(cart)
    except Exception as e:
        #messages.error(request, f'Ocorreu um erro ao processar o pedido {e}')
        print(f'Ocorreu um erro ao processar o pedido: {e}')
        return redirect('checkout')
    
    return redirect('success', order_id=order.id)

@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'sitecompras/success.html', context)