from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User
from .workout import Exercise
from .nutrition import Recipe
from .shop import Product

# -----------------------------------------------------------------------------
# FAVORIS UTILISATEUR
# -----------------------------------------------------------------------------
class Favorite(models.Model):
    """
    Favoris de l'utilisateur (exercices, recettes, produits).
    Permet à l'utilisateur de sauvegarder du contenu pour y accéder facilement.
    """
    CONTENT_TYPE_CHOICES = [
        ('exercise', _('Exercice')),
        ('recipe', _('Recette')),
        ('product', _('Produit')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    
    # Relations polymorphiques (stockées comme IDs)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True, related_name='favorited_by')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True, related_name='favorited_by')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='favorited_by')
    
    # Notes personnelles
    notes = models.TextField(blank=True, help_text="Notes personnelles sur ce favori")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Favori")
        verbose_name_plural = _("Favoris")
        unique_together = ('user', 'content_type', 'exercise', 'recipe', 'product')

    def __str__(self):
        if self.content_type == 'exercise' and self.exercise:
            return f"{self.user.username} - {self.exercise.name}"
        elif self.content_type == 'recipe' and self.recipe:
            return f"{self.user.username} - {self.recipe.title}"
        elif self.content_type == 'product' and self.product:
            return f"{self.user.username} - {self.product.name}"
        return f"{self.user.username} - Favorite"

    @property
    def content(self):
        """Retourne l'objet de contenu (exercice, recette ou produit)"""
        if self.content_type == 'exercise':
            return self.exercise
        elif self.content_type == 'recipe':
            return self.recipe
        elif self.content_type == 'product':
            return self.product
        return None

    @property
    def content_name(self):
        """Retourne le nom du contenu"""
        content = self.content
        if content:
            return content.name if hasattr(content, 'name') else content.title
        return "Unknown"
