from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from web.forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, CustomPasswordChangeForm
from api.models import User
from api.services.gamification import check_and_award_badges

def login_view(request):
    """
    User login.
    Updates streak on login.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Update Streak on Login
            if hasattr(user, 'stats'):
                user.stats.update_streak()
            return redirect('home')
        else:
            messages.error(request, _("Invalid credentials."))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'web/login.html', {'form': form})

def logout_view(request):
    """
    User logout.
    """
    logout(request)
    return redirect('home')

def register_view(request):
    """
    New user registration.
    Initializes stats and streak.
    Sends welcome email.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify authentication backend to avoid "multiple authentication backends" error
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            # Init Streak
            if hasattr(user, 'stats'):
                user.stats.update_streak()
            
            # Send Welcome Email
            try:
                send_mail(
                    subject=_("Welcome to FitWell! ✨"),
                    message=_("Hi %(username)s,\n\nGlad to have you with us. Your journey to a better daily life starts now.\n\nAccess your space: %(url)s\n\nSee you soon,\nThe FitWell Team") % {
                        'username': user.username,
                        'url': request.build_absolute_uri(reverse('dashboard'))
                    },
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
            except Exception:
                pass # Don't block registration if email fails

            messages.success(request, _("Glad to meet you! Your account is ready."))
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'web/register.html', {'form': form})

@login_required(login_url='login')
def profile_view(request):
    # Update Streak on Profile Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/profile.html', {'user': request.user, 'plan': latest_plan})

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your settings have been saved! ✨"))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'web/edit_profile.html', {'form': form})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your new password is active. Your security is ensured. 🔒'))
            return redirect('profile')
        else:
            messages.error(request, _('Oops, check the entered information.'))
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'web/change_password.html', {
        'form': form
    })


@login_required(login_url='login')
def delete_account(request):
    """
    Allows the user to permanently delete their own account.
    Security: requires password confirmation + checkbox.
    Super-user cannot delete themselves this way (platform security).
    """
    if request.method != 'POST':
        return render(request, 'web/delete_account.html')

    # Validation
    password = request.POST.get('password', '')
    confirm = request.POST.get('confirm', '')

    if request.user.is_superuser:
        messages.error(request, _("The super-user cannot delete themselves via this page (security)."))
        return redirect('profile')

    if confirm != 'DELETE':
        messages.error(request, _("Type exactly DELETE to confirm."))
        return redirect('delete_account')

    if not request.user.check_password(password):
        messages.error(request, _("Incorrect password."))
        return redirect('delete_account')

    # Deletion
    username = request.user.username
    logout(request)
    User.objects.filter(username=username).delete()
    messages.success(request, _("Your account %(u)s has been permanently deleted. See you maybe later.") % {'u': username})
    return redirect('home')
