from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# EXERCISE LIBRARY
# -----------------------------------------------------------------------------
class Exercise(models.Model):
    """
    Represents a physical exercise in the library.
    Contains technical details (muscle group, difficulty, equipment).
    """
    MUSCLE_CHOICES = [
        ('chest', _('Chest')),
        ('back', _('Back')),
        ('legs', _('Legs')),
        ('shoulders', _('Shoulders')),
        ('arms', _('Arms')),
        ('abs', _('Abs')),
        ('cardio', _('Cardio')),
        ('full', _('Full Body')),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    equipment = models.CharField(max_length=100, blank=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Additional fields for more details
    instructions = models.TextField(blank=True, help_text="Step by step instructions")
    video_url = models.CharField(max_length=500, blank=True, null=True, help_text="Tutorial video URL")
    calories_per_minute = models.IntegerField(null=True, blank=True, help_text="Calories burned per minute (estimate)")
    is_compound = models.BooleanField(default=False, help_text="Compound exercise vs isolation")
    secondary_muscles = models.JSONField(default=list, blank=True, help_text="Secondary muscle groups targeted")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# -----------------------------------------------------------------------------
# WORKOUT TRACKING
# -----------------------------------------------------------------------------
class WorkoutSession(models.Model):
    """
    Represents a complete workout session.
    Contains all sets performed during the session.
    """
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    total_volume = models.FloatField(default=0.0)  # Total kg lifted (weight * reps)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
    
    def calculate_duration(self):
        """Calculate session duration in minutes"""
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            return int(delta.total_seconds() / 60)
        return 0
    
    def calculate_total_volume(self):
        """Calculate total volume (weight * reps) for all sets"""
        total = 0
        for exercise_set in self.sets.all():
            total += exercise_set.weight * exercise_set.reps
        return total
    
    def complete_session(self):
        """Mark session as completed and calculate stats"""
        from django.utils import timezone
        self.completed_at = timezone.now()
        self.status = 'completed'
        self.duration_minutes = self.calculate_duration()
        self.total_volume = self.calculate_total_volume()
        self.save()
        
        # Award XP to user
        if hasattr(self.user, 'stats'):
            xp_earned = 50 + (self.duration_minutes // 10) * 10  # Base 50 XP + 10 per 10 min
            self.user.stats.add_xp(xp_earned)

class ExerciseSet(models.Model):
    """
    Represents a set of an exercise in a session.
    Contains the number of repetitions and the weight used.
    """
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='performed_sets')
    set_number = models.IntegerField(default=1)
    reps = models.IntegerField()
    weight = models.FloatField(help_text="Weight in kg")
    rest_seconds = models.IntegerField(default=60, help_text="Rest time after set")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.exercise.name} - Set {self.set_number}: {self.reps} reps @ {self.weight}kg"
    
    @property
    def volume(self):
        """Calculate volume for this set (weight * reps)"""
        return self.weight * self.reps
