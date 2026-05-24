from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User
from .workout import Exercise

# -----------------------------------------------------------------------------
# TRAINING PROGRAMS
# -----------------------------------------------------------------------------
class Program(models.Model):
    """
    Structured training program over multiple days or weeks.
    """
    GOAL_CHOICES = [
        ('weight_loss', _('Weight loss')),
        ('muscle_gain', _('Muscle gain')),
        ('strength', _('Strength')),
        ('endurance', _('Endurance')),
        ('mobility', _('Mobility')),
        ('fitness', _('Fitness')),
    ]

    LEVEL_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]

    DURATION_CHOICES = [
        ('7_days', _('7 days')),
        ('4_weeks', _('4 weeks')),
        ('8_weeks', _('8 weeks')),
        ('12_weeks', _('12 weeks')),
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
    
    # Statistics
    total_sessions = models.IntegerField(default=0, help_text="Total number of sessions")
    duration_weeks = models.IntegerField(default=0, help_text="Duration in weeks")
    
    # Tips
    nutrition_tips = models.TextField(blank=True, help_text="Nutritional tips")
    equipment_needed = models.TextField(blank=True, help_text="Required equipment")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProgramDay(models.Model):
    """
    Day of a training program.
    Can be a rest day or a training day.
    """
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField(help_text="Day number in the program")
    
    # Day description
    name = models.CharField(max_length=200, help_text="Ex: Day 1 - Chest & Triceps")
    description = models.TextField(blank=True, help_text="Day description")
    is_rest_day = models.BooleanField(default=False, help_text="True if rest day")
    
    # Estimated duration
    estimated_duration_minutes = models.IntegerField(default=45, help_text="Estimated duration in minutes")

    class Meta:
        ordering = ['day_number']
        verbose_name = _("Program day")
        verbose_name_plural = _("Program days")
        unique_together = ('program', 'day_number')

    def __str__(self):
        return f"{self.program.name} - Day {self.day_number}"


class ProgramExercise(models.Model):
    """
    Exercise in a program day.
    """
    program_day = models.ForeignKey(ProgramDay, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Exercise details in the program
    order = models.IntegerField(default=1, help_text="Exercise order in the day")
    sets = models.IntegerField(default=3, help_text="Number of sets")
    reps = models.CharField(max_length=50, help_text="Ex: 8-12, 15, AMRAP")
    rest_seconds = models.IntegerField(default=60, help_text="Rest time in seconds")
    weight_note = models.CharField(max_length=100, blank=True, help_text="Weight note (ex: 60% 1RM)")
    
    # Notes
    notes = models.TextField(blank=True, help_text="Specific notes for this exercise")

    class Meta:
        ordering = ['order']
        verbose_name = _("Program exercise")
        verbose_name_plural = _("Program exercises")

    def __str__(self):
        return f"{self.program_day.name} - {self.order}. {self.exercise.name}"


# -----------------------------------------------------------------------------
# USER PROGRAM PROGRESSION
# -----------------------------------------------------------------------------
class UserProgramProgress(models.Model):
    """
    Track user progress in a program.
    """
    STATUS_CHOICES = [
        ('not_started', _('Not started')),
        ('in_progress', _('In progress')),
        ('completed', _('Completed')),
        ('abandoned', _('Abandoned')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_progress')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='user_progress')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Progression
    current_day = models.IntegerField(default=1, help_text="Current day in the program")
    days_completed = models.JSONField(default=list, blank=True, help_text="List of completed days")
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'program')
        verbose_name = _("User progression")
        verbose_name_plural = _("User progressions")

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"

    @property
    def progress_percentage(self):
        if self.program.total_sessions == 0:
            return 0
        return int((len(self.days_completed) / self.program.total_sessions) * 100)
