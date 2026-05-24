"""
Signals — captures IP and User-Agent on each user login,
increments login counter. This info is displayed in the
custom admin dashboard (/en/admin-panel/).
"""
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


def get_client_ip(request) -> str:
    """Returns the real client IP (taking into account proxies like Render/Cloudflare)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '') or ''


@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    """On each login: records IP, user-agent, increments counter."""
    if request is None:
        return
    user.last_login_ip = get_client_ip(request) or None
    user.last_user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    user.login_count = (user.login_count or 0) + 1
    user.save(update_fields=['last_login_ip', 'last_user_agent', 'login_count'])
