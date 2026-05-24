from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.models import WellnessPlan

def home(request):
    """
    Site home page.
    Displays the latest generated plan if user is logged in.
    """
    latest_plan = None
    if request.user.is_authenticated:
        latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/home.html', {'plan': latest_plan})

@login_required(login_url='login')
def tools_view(request):
    # Update Streak on Tools Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = None
    if request.user.is_authenticated:
        latest_plan = request.user.plans.order_by('-created_at').first()
        
    return render(request, 'web/tools.html', {'plan': latest_plan})

def legal_view(request):
    """
    Legal notices and terms of use page.
    """
    return render(request, 'web/legal.html')


def about_view(request):
    """
    "About" page: mission, values, FitWell history.
    """
    return render(request, 'web/about.html')

def custom_404(request, exception):
    """
    Custom 404 error page (Page not found).
    """
    return render(request, '404.html', status=404)

def custom_500(request):
    """
    Custom 500 error page (Server error).
    """
    return render(request, '500.html', status=500)
