from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from api.models import WellnessPlan
from api.services import generate_wellness_plan
from api.services.gamification import check_and_award_badges

@login_required(login_url='login')
def onboarding_welcome(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    return render(request, 'web/onboarding/welcome.html')

@login_required(login_url='login')
def onboarding_step1(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        request.session['onboarding_goal'] = request.POST.get('goal')
        return redirect('onboarding_step2')
    
    return render(request, 'web/onboarding/step1_goal.html')

@login_required(login_url='login')
def onboarding_step2(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        request.session['onboarding_activity'] = request.POST.get('activity_level')
        return redirect('onboarding_step3')
    
    return render(request, 'web/onboarding/step2_level.html')

@login_required(login_url='login')
def onboarding_step3(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = int(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        goal = request.session.get('onboarding_goal', 'maintenance')
        activity_level = request.session.get('onboarding_activity', 'moderate')
        
        workout_plan, nutrition_plan, health_score = generate_wellness_plan(
            age=age, gender=gender, height=height, weight=weight,
            goal=goal, activity_level=activity_level
        )
        
        plan = WellnessPlan.objects.create(
            user=request.user,
            age=age, gender=gender, height=height, weight=weight,
            goal=goal, activity_level=activity_level,
            workout_plan=workout_plan,
            nutrition_plan=nutrition_plan
        )
        
        if hasattr(request.user, 'stats'):
            request.user.stats.health_score = health_score
            
            # Update breakdown scores from analysis
            if 'analysis' in workout_plan and 'breakdown' in workout_plan['analysis']:
                breakdown = workout_plan['analysis']['breakdown']
                request.user.stats.fitness_score = breakdown.get('fitness', 0)
                request.user.stats.recovery_score = breakdown.get('recovery', 0)
                request.user.stats.lifestyle_score = breakdown.get('lifestyle', 0)
                if 'consistency' in breakdown:
                    request.user.stats.consistency_score = breakdown.get('consistency', 0)

            request.user.stats.add_xp(100)
            request.user.stats.update_streak()
        
        new_badges = check_and_award_badges(request.user)
        
        request.user.is_onboarded = True
        request.user.save()
        
        request.session.pop('onboarding_goal', None)
        request.session.pop('onboarding_activity', None)
        
        return render(request, 'web/onboarding/complete.html', {
            'message': _("Congratulations! Your balance is ready. +%(xp)s") % {'xp': 100},
            'plan': plan,
            'new_badges': new_badges
        })
    
    return render(request, 'web/onboarding/step3_data.html')
