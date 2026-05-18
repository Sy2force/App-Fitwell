from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# -----------------------------------------------------------------------------
# NUTRITION / RECETTES
# -----------------------------------------------------------------------------
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', _('Facile')),
        ('medium', _('Moyen')),
        ('hard', _('Difficile')),
    ]
    
    CATEGORY_CHOICES = [
        ('breakfast', _('Petit déjeuner')),
        ('lunch', _('Déjeuner')),
        ('dinner', _('Dîner')),
        ('snack', _('Collation')),
        ('shake', _('Shake / Smoothie')),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    prep_time_minutes = models.IntegerField(default=15)
    calories = models.IntegerField(default=0)
    protein_g = models.IntegerField(default=0)
    carbs_g = models.IntegerField(default=0)
    fats_g = models.IntegerField(default=0)
    
    ingredients = models.TextField(help_text="Liste des ingrédients séparés par des sauts de ligne")
    instructions = models.TextField(help_text="Étapes de préparation")
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Champs supplémentaires
    servings = models.IntegerField(default=1, help_text="Nombre de portions")
    fiber_g = models.IntegerField(default=0, help_text="Fibres en grammes")
    sugar_g = models.IntegerField(default=0, help_text="Sucres en grammes")
    sodium_mg = models.IntegerField(default=0, help_text="Sodium en milligrammes")
    tags = models.JSONField(default=list, blank=True, help_text="Tags pour le filtrage (ex: vegan, gluten-free)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
