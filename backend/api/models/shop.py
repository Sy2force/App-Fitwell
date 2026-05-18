from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# BOUTIQUE SPORT (E-COMMERCE DÉMO)
# -----------------------------------------------------------------------------
class Product(models.Model):
    """
    Produits de la boutique sport fictive.
    Mode démo : pas de vrai paiement, mais logique e-commerce crédible.
    """
    CATEGORY_CHOICES = [
        ('strength', _('Musculation')),
        ('cardio', _('Cardio')),
        ('yoga', _('Yoga & Mobilité')),
        ('running', _('Running')),
        ('clothing', _('Vêtements')),
        ('accessories', _('Accessoires')),
        ('nutrition', _('Nutrition Sportive')),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Descriptions
    description_short = models.CharField(max_length=200, help_text="Description courte pour les cartes")
    description_long = models.TextField(help_text="Description détaillée du produit")
    
    # Prix
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix en EUR")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Prix barré si promo")
    
    # Images
    image = models.CharField(max_length=500, blank=True, null=True, help_text="URL de l'image principale")
    gallery = models.JSONField(default=list, blank=True, help_text="Liste d'URLs d'images additionnelles")
    
    # Évaluation & Stock
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5, help_text="Note moyenne sur 5")
    stock = models.IntegerField(default=10, help_text="Stock disponible")
    
    # Marque & Caractéristiques
    brand = models.CharField(max_length=100, blank=True, help_text="Marque du produit")
    features = models.JSONField(default=list, blank=True, help_text="Liste des caractéristiques")
    
    # Recommandations
    recommended_for = models.TextField(blank=True, help_text="Pour qui ce produit est recommandé")
    related_exercises = models.ManyToManyField('Exercise', blank=True, related_name='recommended_products')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

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
# PANIER (CART)
# -----------------------------------------------------------------------------
class Cart(models.Model):
    """
    Panier d'achat de l'utilisateur.
    Mode démo : pas de persistance réelle sur le long terme.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Paniers")

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
    Article dans le panier.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Article du panier")
        verbose_name_plural = _("Articles du panier")
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


# -----------------------------------------------------------------------------
# COMMANDES (ORDERS)
# -----------------------------------------------------------------------------
class Order(models.Model):
    """
    Commande de l'utilisateur (mode démo).
    """
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('processing', _('En préparation')),
        ('shipped', _('Expédié')),
        ('delivered', _('Livré')),
        ('cancelled', _('Annulé')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    
    # Adresse de livraison (mode démo)
    shipping_address = models.TextField(help_text="Adresse de livraison")
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='France')
    
    # Montants
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Commande")
        verbose_name_plural = _("Commandes")

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{self.user.id}-{self.created_at.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Article dans une commande.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix au moment de la commande")

    class Meta:
        verbose_name = _("Article de commande")
        verbose_name_plural = _("Articles de commande")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.price * self.quantity
