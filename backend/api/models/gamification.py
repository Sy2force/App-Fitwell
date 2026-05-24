from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# GAMIFICATION & STATS
# -----------------------------------------------------------------------------
class UserStats(models.Model):
    """
    User statistics and progression.
    Linked in OneToOne with User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    current_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    health_score = models.IntegerField(default=0)
    
    # Detailed scores (Radar Chart)
    fitness_score = models.IntegerField(default=0)
    recovery_score = models.IntegerField(default=0)
    lifestyle_score = models.IntegerField(default=0)
    consistency_score = models.IntegerField(default=0)

    def update_streak(self):
        """
        Updates the current streak based on last activity date.
        Should be called whenever a significant action (login, plan generation) occurs.
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.last_activity_date == today:
            return # Already counted for today
            
        if self.last_activity_date == today - timezone.timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
            
        self.last_activity_date = today
        self.save()

    def add_xp(self, amount):
        """
        Adds XP and handles leveling up.
        """
        self.xp += amount
        
        # Formula: Level N requires N * 500 XP
        required_xp = self.level * 500
        
        while self.xp >= required_xp:
            self.xp -= required_xp
            self.level += 1
            required_xp = self.level * 500
            
        self.save()

    @property
    def xp_threshold(self):
        return self.level * 500

    @property
    def xp_progress(self):
        if self.xp_threshold == 0: return 0
        return int((self.xp / self.xp_threshold) * 100)

    @property
    def xp_remaining(self):
        return self.xp_threshold - self.xp

    def __str__(self):
        return f"Stats for {self.user.username}"

# -----------------------------------------------------------------------------
# BADGES & ACHIEVEMENTS
# -----------------------------------------------------------------------------
class Badge(models.Model):
    """
    Badges unlockable by users.
    """
    CATEGORY_CHOICES = [
        ('workout', _('Workout')),
        ('streak', _('Consistency')),
        ('social', _('Social')),
        ('milestone', _('Milestone')),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, default='🏆')
    condition_type = models.CharField(max_length=50)
    condition_value = models.IntegerField()
    xp_reward = models.IntegerField(default=100)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.icon} {self.name}"

class UserBadge(models.Model):
    """
    Badges unlocked by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

# Signal to create UserStats automatically
@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    if hasattr(instance, 'stats'):
        instance.stats.save()
