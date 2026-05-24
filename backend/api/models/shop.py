from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# SPORTS SHOP (DEMO E-COMMERCE)
# -----------------------------------------------------------------------------
class Product(models.Model):
    """
    Products from the fictional sports shop.
    Demo mode: no real payment, but credible e-commerce logic.
    """
    CATEGORY_CHOICES = [
        ('strength', _('Bodybuilding')),
        ('cardio', _('Cardio')),
        ('yoga', _('Yoga & Mobility')),
        ('running', _('Running')),
        ('clothing', _('Clothing')),
        ('accessories', _('Accessories')),
        ('nutrition', _('Sports Nutrition')),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Descriptions
    description_short = models.CharField(max_length=200, help_text="Short description for cards")
    description_long = models.TextField(help_text="Detailed product description")
    
    # Price
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in EUR")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Strikethrough price if on sale")
    
    # Images
    image = models.CharField(max_length=500, blank=True, null=True, help_text="Main image URL")
    gallery = models.JSONField(default=list, blank=True, help_text="List of additional image URLs")
    
    # Rating & Stock
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5, help_text="Average rating out of 5")
    stock = models.IntegerField(default=10, help_text="Available stock")
    
    # Brand & Features
    brand = models.CharField(max_length=100, blank=True, help_text="Product brand")
    features = models.JSONField(default=list, blank=True, help_text="List of features")
    
    # Recommendations
    recommended_for = models.TextField(blank=True, help_text="Who this product is recommended for")
    related_exercises = models.ManyToManyField('Exercise', blank=True, related_name='recommended_products')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name}" if self.brand else self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


# -----------------------------------------------------------------------------
# CART
# -----------------------------------------------------------------------------
class Cart(models.Model):
    """
    User shopping cart.
    Demo mode: no real long-term persistence.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Item in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Cart item")
        verbose_name_plural = _("Cart items")
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


# -----------------------------------------------------------------------------
# ORDERS
# -----------------------------------------------------------------------------
class Order(models.Model):
    """
    User order (demo mode).
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    
    # Shipping address (demo mode)
    shipping_address = models.TextField(help_text="Shipping address")
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='France')
    
    # Amounts
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{self.user.id}-{self.created_at.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Item in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at time of order")

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.price * self.quantity
