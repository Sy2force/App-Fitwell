from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User
from .workout import Exercise

# -----------------------------------------------------------------------------
# PROGRAMMES D'ENTRAÎNEMENT
# -----------------------------------------------------------------------------
class Program(models.Model):
    """
    Programme d'entraînement structuré sur plusieurs jours ou semaines.
    """
    GOAL_CHOICES = [
        ('weight_loss', _('Perte de poids')),
        ('muscle_gain', _('Prise de muscle')),
        ('strength', _('Force')),
        ('endurance', _('Endurance')),
        ('mobility', _('Mobilité')),
        ('fitness', _('Remise en forme')),
    ]

    LEVEL_CHOICES = [
        ('beginner', _('Débutant')),
        ('intermediate', _('Intermédiaire')),
        ('advanced', _('Avancé')),
    ]

    DURATION_CHOICES = [
        ('7_days', _('7 jours')),
        ('4_weeks', _('4 semaines')),
        ('8_weeks', _('8 semaines')),
        ('12_weeks', _('12 semaines')),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    
    # Description
    description_short = models.CharField(max_length=200)
    description_long = models.TextField()
    
    # Image
    image = models.CharField(max_length=500, blank=True, null=True)
    
    # Statistiques
    total_sessions = models.IntegerField(default=0, help_text="Nombre total de séances")
    duration_weeks = models.IntegerField(default=0, help_text="Durée en semaines")
    
    # Conseils
    nutrition_tips = models.TextField(blank=True, help_text="Conseils nutritionnels")
    equipment_needed = models.TextField(blank=True, help_text="Matériel nécessaire")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Programme")
        verbose_name_plural = _("Programmes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProgramDay(models.Model):
    """
    Jour d'un programme d'entraînement.
    Peut être un jour de repos ou un jour d'entraînement.
    """
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField(help_text="Numéro du jour dans le programme")
    
    # Description du jour
    name = models.CharField(max_length=200, help_text="Ex: Jour 1 - Pectoraux & Triceps")
    description = models.TextField(blank=True, help_text="Description du jour")
    is_rest_day = models.BooleanField(default=False, help_text="Vrai si jour de repos")
    
    # Durée estimée
    estimated_duration_minutes = models.IntegerField(default=45, help_text="Durée estimée en minutes")

    class Meta:
        ordering = ['day_number']
        verbose_name = _("Jour de programme")
        verbose_name_plural = _("Jours de programme")
        unique_together = ('program', 'day_number')

    def __str__(self):
        return f"{self.program.name} - Day {self.day_number}"


class ProgramExercise(models.Model):
    """
    Exercice dans un jour de programme.
    """
    program_day = models.ForeignKey(ProgramDay, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Détails de l'exercice dans le programme
    order = models.IntegerField(default=1, help_text="Ordre de l'exercice dans le jour")
    sets = models.IntegerField(default=3, help_text="Nombre de séries")
    reps = models.CharField(max_length=50, help_text="Ex: 8-12, 15, AMRAP")
    rest_seconds = models.IntegerField(default=60, help_text="Temps de repos en secondes")
    weight_note = models.CharField(max_length=100, blank=True, help_text="Note sur le poids (ex: 60% 1RM)")
    
    # Notes
    notes = models.TextField(blank=True, help_text="Notes spécifiques pour cet exercice")

    class Meta:
        ordering = ['order']
        verbose_name = _("Exercice de programme")
        verbose_name_plural = _("Exercices de programme")

    def __str__(self):
        return f"{self.program_day.name} - {self.order}. {self.exercise.name}"


# -----------------------------------------------------------------------------
# PROGRESSION UTILISATEUR DANS PROGRAMME
# -----------------------------------------------------------------------------
class UserProgramProgress(models.Model):
    """
    Suivi de la progression d'un utilisateur dans un programme.
    """
    STATUS_CHOICES = [
        ('not_started', _('Non commencé')),
        ('in_progress', _('En cours')),
        ('completed', _('Terminé')),
        ('abandoned', _('Abandonné')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_progress')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='user_progress')
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Progression
    current_day = models.IntegerField(default=1, help_text="Jour actuel dans le programme")
    days_completed = models.JSONField(default=list, blank=True, help_text="Liste des jours complétés")
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'program')
        verbose_name = _("Progression utilisateur")
        verbose_name_plural = _("Progressions utilisateurs")

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"

    @property
    def progress_percentage(self):
        if self.program.total_sessions == 0:
            return 0
        return int((len(self.days_completed) / self.program.total_sessions) * 100)
