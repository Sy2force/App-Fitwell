from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# -----------------------------------------------------------------------------
# NUTRITION / RECIPES
# -----------------------------------------------------------------------------
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    ]
    
    CATEGORY_CHOICES = [
        ('breakfast', _('Breakfast')),
        ('lunch', _('Lunch')),
        ('dinner', _('Dinner')),
        ('snack', _('Snack')),
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
    
    ingredients = models.TextField(help_text="List of ingredients separated by line breaks")
    instructions = models.TextField(help_text="Preparation steps")
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Additional fields
    servings = models.IntegerField(default=1, help_text="Number of servings")
    fiber_g = models.IntegerField(default=0, help_text="Fiber in grams")
    sugar_g = models.IntegerField(default=0, help_text="Sugars in grams")
    sodium_mg = models.IntegerField(default=0, help_text="Sodium in milligrams")
    tags = models.JSONField(default=list, blank=True, help_text="Tags for filtering (e.g. vegan, gluten-free)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
