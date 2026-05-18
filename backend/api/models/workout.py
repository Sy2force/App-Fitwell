from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# BIBLIOTHÈQUE D'EXERCICES
# -----------------------------------------------------------------------------
class Exercise(models.Model):
    """
    Représente un exercice physique dans la bibliothèque.
    Contient les détails techniques (groupe musculaire, difficulté, équipement).
    """
    MUSCLE_CHOICES = [
        ('chest', _('Pectoraux')),
        ('back', _('Dos')),
        ('legs', _('Jambes')),
        ('shoulders', _('Épaules')),
        ('arms', _('Bras')),
        ('abs', _('Abdominaux')),
        ('cardio', _('Cardio')),
        ('full', _('Corps complet')),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', _('Débutant')),
        ('intermediate', _('Intermédiaire')),
        ('advanced', _('Avancé')),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    equipment = models.CharField(max_length=100, blank=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Champs supplémentaires pour plus de détails
    instructions = models.TextField(blank=True, help_text="Instructions étape par étape")
    video_url = models.CharField(max_length=500, blank=True, null=True, help_text="URL de la vidéo tutoriel")
    calories_per_minute = models.IntegerField(null=True, blank=True, help_text="Calories brûlées par minute (estimation)")
    is_compound = models.BooleanField(default=False, help_text="Exercice polyarticulaire vs isolation")
    secondary_muscles = models.JSONField(default=list, blank=True, help_text="Groupes musculaires secondaires sollicités")
    
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
    Représente une séance d'entraînement complète.
    Contient tous les sets effectués pendant la session.
    """
    STATUS_CHOICES = [
        ('active', _('En cours')),
        ('completed', _('Terminée')),
        ('cancelled', _('Annulée')),
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
    Représente une série d'un exercice dans une séance.
    Contient le nombre de répétitions et le poids utilisé.
    """
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='performed_sets')
    set_number = models.IntegerField(default=1)
    reps = models.IntegerField()
    weight = models.FloatField(help_text="Poids en kg")
    rest_seconds = models.IntegerField(default=60, help_text="Temps de repos après la série")
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
