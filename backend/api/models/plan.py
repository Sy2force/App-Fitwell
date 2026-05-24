from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

# -----------------------------------------------------------------------------
# PLANNER / WELLNESS
# -----------------------------------------------------------------------------
class CustomEvent(models.Model):
    """
    Custom events for planning (Sport, Work, etc.)
    """
    TYPE_CHOICES = [
        ('sport', _('Sport & fitness')),
        ('work', _('Work & career')),
        ('lifestyle', _('Personal life & leisure')),
        ('nutrition', _('Nutrition')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_events')
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='work')
    day_of_week = models.CharField(max_length=10, blank=True, null=True) # e.g., 'monday'
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class WellnessPlan(models.Model):
    """
    AI generated plan.
    Stores biometric data and JSON result.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    
    # Choices
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]
    
    GOAL_CHOICES = [
        ('weight_loss', _('Weight loss')),
        ('muscle_gain', _('Muscle gain')),
        ('maintenance', _('Maintenance')),
    ]
    
    ACTIVITY_CHOICES = [
        ('sedentary', _('Sedentary (little or no exercise)')),
        ('moderate', _('Moderate (1-3 times per week)')),
        ('active', _('Active (3-5 times per week)')),
        ('elite', _('Elite (6-7 times per week)')),
    ]
    
    # Inputs
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.IntegerField() # cm
    weight = models.FloatField() # kg
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    
    # Generated Outputs (JSON)
    workout_plan = models.JSONField(default=dict)
    nutrition_plan = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan for {self.user.username} ({self.created_at})"

# -----------------------------------------------------------------------------
# DAILY TRACKING (DAILY LOG)
# -----------------------------------------------------------------------------
class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(auto_now_add=True)
    
    # Metrics
    water_liters = models.FloatField(default=0.0)
    sleep_hours = models.FloatField(default=0.0)
    mood = models.IntegerField(default=5) # 1-10
    weight = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Log {self.user.username} - {self.date}"
