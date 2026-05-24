from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------------------------------------------------------
# CUSTOM USER
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    Extend the base Django user to add:
    - Profile: bio + avatar URL
    - Marketing / verification flags
    - Connection tracking: IP, user agent, login count (visible in admin dashboard)
    - Soft delete: is_hidden (hide without deleting)
    """
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True, null=True)

    # Marketing / admin fields
    marketing_opt_in = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    # ----- Connection tracking (visible in custom admin dashboard) -----
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, help_text="IP of last connection")
    last_user_agent = models.CharField(max_length=500, blank=True, default="", help_text="User-Agent of last connection")
    login_count = models.PositiveIntegerField(default=0, help_text="Total number of connections")

    # ----- Soft delete (hide without deleting) -----
    is_hidden = models.BooleanField(default=False, help_text="Hidden by admin (equivalent soft-delete)")

    def __str__(self):
        return self.username
