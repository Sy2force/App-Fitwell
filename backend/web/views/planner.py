from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from web.forms import WellnessPlanForm, CustomEventForm
from api.models import WellnessPlan, CustomEvent
from api.services import generate_wellness_plan
from api.services.gamification import check_and_award_badges

@login_required(login_url='login')
def planner_view(request):
    # Update Streak on Planner Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    plans = request.user.plans.order_by('-created_at')
    latest_plan = plans.first()
    
    if request.method == 'POST':
        form = WellnessPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            
            # Generate plan via service
            workout, nutrition, score = generate_wellness_plan(
                plan.age, plan.gender, plan.height, plan.weight, plan.goal, plan.activity_level
            )
            
            plan.workout_plan = workout
            plan.nutrition_plan = nutrition
            plan.save()
            
            # Update user stats
            if hasattr(request.user, 'stats'):
                request.user.stats.health_score = score
                
                # Update breakdown scores from analysis
                if 'analysis' in workout and 'breakdown' in workout['analysis']:
                    breakdown = workout['analysis']['breakdown']
                    request.user.stats.fitness_score = breakdown.get('fitness', 0)
                    request.user.stats.recovery_score = breakdown.get('recovery', 0)
                    request.user.stats.lifestyle_score = breakdown.get('lifestyle', 0)
                    request.user.stats.consistency_score = breakdown.get('consistency', 0)
                
                # Gamification: +100 XP for taking action
                request.user.stats.add_xp(100)
                
                # Update Streak (Explicit update on action)
                request.user.stats.update_streak()
                
                # Badge Trigger
                check_and_award_badges(request.user)
                
            messages.success(request, _("Your program is ready! +100 energy"))
            return redirect('planner')
    else:
        if latest_plan:
            # Pre-fill form with latest plan data
            initial_data = {
                'age': latest_plan.age,
                'gender': latest_plan.gender,
                'height': latest_plan.height,
                'weight': latest_plan.weight,
                'goal': latest_plan.goal,
                'activity_level': latest_plan.activity_level,
            }
            form = WellnessPlanForm(initial=initial_data)
        else:
            form = WellnessPlanForm()

    return render(request, 'web/planner.html', {'plan': latest_plan, 'plans': plans, 'form': form})


@login_required(login_url='login')
def custom_planner_view(request):
    # Update Streak
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    events = request.user.custom_events.order_by('start_time')
    
    # Organize by day for the template
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekly_events = {day: [] for day in days}
    for event in events:
        if event.day_of_week in weekly_events:
            weekly_events[event.day_of_week].append(event)
            
    if request.method == 'POST':
        form = CustomEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, _("Activité ajoutée à ton planning !"))
            return redirect('custom_planner')
    else:
        form = CustomEventForm()
        
    return render(request, 'web/custom_planner.html', {
        'form': form,
        'weekly_events': weekly_events,
        'days': days
    })

@login_required(login_url='login')
def delete_custom_event(request, event_id):
    event = get_object_or_404(CustomEvent, id=event_id, user=request.user)
    event.delete()
    messages.success(request, _("Activity deleted."))
    return redirect('custom_planner')

@login_required(login_url='login')
@require_POST
def complete_custom_event(request, event_id):
    event = get_object_or_404(CustomEvent, id=event_id, user=request.user)
    
    if not event.is_completed:
        event.is_completed = True
        event.save()
        
        # Gamification Logic
        xp_gain = 50 # Base XP
        if event.priority == 'high':
            xp_gain = 100
        elif event.priority == 'medium':
            xp_gain = 75
            
        request.user.stats.add_xp(xp_gain)
        
        return JsonResponse({
            'status': 'success',
            'xp_gain': xp_gain,
            'new_xp': request.user.stats.xp,
            'new_level': request.user.stats.level,
            'message': _("Done! +%(xp)s") % {'xp': xp_gain}
        })
        
    return JsonResponse({'status': 'already_completed'})
