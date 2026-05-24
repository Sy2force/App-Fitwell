from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models import Product, Cart, CartItem, Order, OrderItem


def shop_list(request):
    """
    List of all shop products.
    Filters by category, price, rating.
    """
    products = Product.objects.all()
    
    # Filters
    category_filter = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')
    
    if category_filter:
        products = products.filter(category=category_filter)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description_short__icontains=search) |
            Q(brand__icontains=search)
        )
    
    context = {
        'products': products,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'search': search,
    }
    return render(request, 'web/shop_list.html', context)


def shop_detail(request, slug):
    """
    Product detail with complete information.
    """
    product = get_object_or_404(Product, slug=slug)
    
    # Related products (same category)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'web/shop_detail.html', context)


@login_required
def cart_view(request):
    """
    User shopping cart.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'web/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart.
    """
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product is already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def update_cart_quantity(request, item_id):
    """
    Update the quantity of an item in the cart.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = request.POST.get('quantity', 1)
        
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            elif quantity == 0:
                cart_item.delete()
        except ValueError:
            pass
    
    return redirect('cart')


@login_required
def fake_checkout(request):
    """
    Fake payment process (demo mode).
    """
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.items.count() == 0:
        return redirect('cart')
    
    # Create a fake order
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price,
        shipping_cost=0,
        shipping_address="Demo address",
        shipping_city="Paris",
        shipping_postal_code="75001",
        shipping_country="France",
        status='processing'
    )
    
    # Add items to the order
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    
    # Clear the cart
    cart.items.all().delete()
    
    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    """
    Order confirmation page.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'web/order_success.html', context)
