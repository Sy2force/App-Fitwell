from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import random
from web.forms import CustomWorkoutForm
from api.models import Exercise, WorkoutSession, ExerciseSet, DailyLog, Recipe
from api.services.gamification import check_and_award_badges
from django.utils import timezone

@login_required(login_url='login')
def workout_setup_view(request):
    """
    Configuration page before starting a session.
    Allows choosing exercises and duration.
    """
    form = CustomWorkoutForm()
    return render(request, 'web/workout_setup.html', {'form': form})

@login_required(login_url='login')
def workout_session_view(request):
    """
    Live Studio (Workout session).
    Generates an exercise sequence (Warm-up -> Exercises -> Rest -> Cool-down).
    If no exercise is selected, AI chooses according to profile.
    """
    # Logic to build a session
    
    # Defaults
    work_duration = 45
    rest_duration = 15
    selected_exercises_objs = []
    
    # 1. Check if we have data from Setup (POST)
    if request.method == 'POST':
        form = CustomWorkoutForm(request.POST)
        if form.is_valid():
            selected_exercises_objs = list(form.cleaned_data['exercises'])
            work_duration = form.cleaned_data['work_duration']
            rest_duration = form.cleaned_data['rest_duration']
    
    # 2. If no exercises selected (GET or empty POST), fallback to auto-gen logic
    if not selected_exercises_objs:
        # 1. Get User Level/Plan
        user_level = 'beginner'
        if hasattr(request.user, 'stats') and request.user.stats.level > 5:
            user_level = 'intermediate'
        if hasattr(request.user, 'stats') and request.user.stats.level > 15:
            user_level = 'advanced'
            
        # 2. Select Exercises & Sequence Strategy (optimized)
        latest_plan = request.user.plans.only('goal').order_by('-created_at').first()
        goal = latest_plan.goal if latest_plan else 'maintenance'
        
        # Filter exercises by level first (optimized with only)
        base_exercises = Exercise.objects.filter(difficulty=user_level).only('name', 'muscle_group', 'difficulty', 'description', 'image_url')
        if not base_exercises.exists():
            base_exercises = Exercise.objects.all()
            
        # Strategy based on Goal
        if goal == 'weight_loss':
            # High intensity, focus on Cardio/Full Body/Legs
            work_duration = 40
            rest_duration = 10
            priority_groups = ['cardio', 'full', 'legs', 'abs']
            candidates = base_exercises.filter(muscle_group__in=priority_groups)
            if candidates.count() < 5:
                candidates = base_exercises
        elif goal == 'muscle_gain':
            # Hypertrophy, focus on Upper/Lower split elements
            work_duration = 50
            rest_duration = 20
            priority_groups = ['chest', 'back', 'legs', 'shoulders']
            candidates = base_exercises.filter(muscle_group__in=priority_groups)
            if candidates.count() < 5:
                candidates = base_exercises
        else: # maintenance
            candidates = base_exercises

        # Select 5 exercises
        candidate_list = list(candidates)
        if len(candidate_list) > 5:
            selected_exercises_objs = random.sample(candidate_list, 5)
        else:
            selected_exercises_objs = candidate_list
        
    # Build Sequence
    sequence = []
    
    # Warmup
    sequence.append({
        'type': 'warmup',
        'name': _("Joint warm-up"),
        'duration': 60,
        'description': _("Arm, wrist, ankle and hip rotations.")
    })
    
    for ex in selected_exercises_objs:
        # Exercise
        sequence.append({
            'type': 'exercise',
            'name': ex.name,
            'duration': work_duration,
            'description': ex.description,
            'image': ex.image_url or ''
        })
        # Rest
        sequence.append({
            'type': 'rest',
            'name': _("Recovery"),
            'duration': rest_duration,
            'description': _("Breathe deeply. Prepare for the next exercise.")
        })
        
    # Cooldown
    sequence.append({
        'type': 'cooldown',
        'name': _("Cool-down"),
        'duration': 60,
        'description': _("Light stretching and breathing.")
    })
    
    # Post-Workout Nutrition Recommendation
    post_workout_meal = Recipe.objects.filter(category__in=['shake', 'snack']).order_by('?').first()
    if not post_workout_meal:
        post_workout_meal = Recipe.objects.order_by('?').first()
    
    return render(request, 'web/workout_session.html', {
        'sequence': sequence,
        'total_time': sum(s['duration'] for s in sequence) // 60,
        'post_workout_meal': post_workout_meal
    })

@login_required(login_url='login')
@require_POST
def complete_workout(request):
    """
    API endpoint to record a completed workout session.
    Awards energy, updates streak, and logs entry in DailyLog.
    """
    # 1. Award energy and Update Streak
    energy_gain = 100
    if hasattr(request.user, 'stats'):
        request.user.stats.add_xp(energy_gain)
        request.user.stats.update_streak()
    
    # 2. Add entry to Daily Log
    today_log, created = DailyLog.objects.get_or_create(user=request.user, date=timezone.now().date())
    timestamp = timezone.now().strftime("%H:%M")
    log_entry = f"[{timestamp}] { _('Studio session completed') } (+{energy_gain})"
    
    if today_log.notes:
        today_log.notes += f"\n{log_entry}"
    else:
        today_log.notes = log_entry
    today_log.save()
    
    return JsonResponse({
        'status': 'success',
        'energy_gain': energy_gain,
        'new_energy': request.user.stats.xp,
        'new_level': request.user.stats.level,
        'message': _("Well done! +%(xp)s energy") % {'xp': energy_gain}
    })

@login_required(login_url='login')
def start_workout(request):
    """
    Page to start a new workout session.
    Checks there is no active session before creating a new one.
    """
    active_session = WorkoutSession.objects.filter(user=request.user, status='active').first()
    
    if active_session:
        messages.warning(request, _("You already have a session in progress. Finish it first."))
        return redirect('workout_session_detail', session_id=active_session.id)
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        session = WorkoutSession.objects.create(user=request.user, notes=notes)
        messages.success(request, _("Let's go! Enjoy your movement! ✨"))
        return redirect('workout_session_detail', session_id=session.id)
    
    latest_plan = request.user.plans.order_by('-created_at').first()
    suggested_exercises = Exercise.objects.all()[:6]
    
    return render(request, 'web/workout/start.html', {
        'suggested_exercises': suggested_exercises,
        'latest_plan': latest_plan
    })

@login_required(login_url='login')
def workout_session(request, session_id):
    """
    Current session page.
    Displays timer, performed exercises and allows adding sets.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        messages.warning(request, _("This session is already completed."))
        return redirect('workout_history')
    
    # Optimized: only to load only necessary fields
    exercises = Exercise.objects.only('id', 'name', 'muscle_group').order_by('muscle_group', 'name')
    
    # Optimized: prefetch sets with exercises
    sets_by_exercise = {}
    for exercise_set in session.sets.select_related('exercise').only(
        'id', 'set_number', 'reps', 'weight', 'rest_seconds', 'created_at', 'exercise__name'
    ).order_by('created_at'):
        ex_name = exercise_set.exercise.name
        if ex_name not in sets_by_exercise:
            sets_by_exercise[ex_name] = []
        sets_by_exercise[ex_name].append(exercise_set)
    
    return render(request, 'web/workout/session.html', {
        'session': session,
        'exercises': exercises,
        'sets_by_exercise': sets_by_exercise,
        'total_sets': session.sets.count()
    })

@login_required(login_url='login')
@require_POST
def add_set_to_session(request, session_id):
    """
    API endpoint to add a set to an active session (Ajax).
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        return JsonResponse({'error': 'Session not active'}, status=400)
    
    try:
        exercise_id = int(request.POST.get('exercise_id'))
        reps = int(request.POST.get('reps'))
        weight = float(request.POST.get('weight'))
        rest_seconds = int(request.POST.get('rest_seconds', 60))
        notes = request.POST.get('notes', '')
        
        exercise = get_object_or_404(Exercise, id=exercise_id)
        
        last_set = session.sets.filter(exercise=exercise).order_by('-set_number').first()
        set_number = (last_set.set_number + 1) if last_set else 1
        
        exercise_set = ExerciseSet.objects.create(
            session=session,
            exercise=exercise,
            set_number=set_number,
            reps=reps,
            weight=weight,
            rest_seconds=rest_seconds,
            notes=notes
        )
        
        return JsonResponse({
            'status': 'success',
            'set': {
                'id': exercise_set.id,
                'exercise_name': exercise.name,
                'set_number': set_number,
                'reps': reps,
                'weight': weight,
                'volume': exercise_set.volume,
                'rest_seconds': rest_seconds
            },
            'total_sets': session.sets.count()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required(login_url='login')
@require_POST
def complete_workout_session(request, session_id):
    """
    End a workout session.
    Calculates stats and awards energy.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        return JsonResponse({'error': 'Session already completed'}, status=400)
    
    session.complete_session()
    
    new_badges = check_and_award_badges(request.user)
    
    energy_earned = 50 + (session.duration_minutes // 10) * 10
    
    return JsonResponse({
        'status': 'success',
        'message': _("Session completed successfully! 🎉"),
        'energy_earned': energy_earned,
        'duration_minutes': session.duration_minutes,
        'total_volume': round(session.total_volume, 2),
        'total_sets': session.sets.count(),
        'redirect_url': '/workout/history/'
    })

@login_required(login_url='login')
def workout_history(request):
    """
    Workout session history.
    Displays all completed sessions with statistics.
    """
    # Optimized: only to load only necessary fields
    sessions = WorkoutSession.objects.filter(
        user=request.user,
        status='completed'
    ).prefetch_related('sets__exercise').only(
        'id', 'started_at', 'duration_minutes', 'total_volume', 'status'
    ).order_by('-started_at')
    
    # Calculate overall stats
    total_sessions = sessions.count()
    total_volume = sum(s.total_volume for s in sessions)
    total_duration = sum(s.duration_minutes for s in sessions)
    
    # Recent sessions for charts (last 10)
    recent_sessions = sessions[:10]
    chart_dates = [s.started_at.strftime('%d/%m') for s in reversed(list(recent_sessions))]
    chart_volume = [s.total_volume for s in reversed(list(recent_sessions))]
    chart_duration = [s.duration_minutes for s in reversed(list(recent_sessions))]
    
    return render(request, 'web/workout/history.html', {
        'sessions': sessions[:20],  # Show last 20 sessions
        'total_sessions': total_sessions,
        'total_volume': round(total_volume, 2),
        'total_duration': total_duration,
        'avg_duration': round(total_duration / total_sessions, 2) if total_sessions > 0 else 0,
        'avg_volume': round(total_volume / total_sessions, 2) if total_sessions > 0 else 0,
        'chart_dates': chart_dates,
        'chart_volume': chart_volume,
        'chart_duration': chart_duration
    })

@login_required(login_url='login')
def workout_detail(request, session_id):
    """
    Details of a specific session.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    # Group sets by exercise (optimized)
    sets_by_exercise = {}
    for exercise_set in session.sets.select_related('exercise').only(
        'id', 'set_number', 'reps', 'weight', 'rest_seconds', 'created_at', 'exercise__name', 'exercise__muscle_group'
    ).order_by('created_at'):
        ex_name = exercise_set.exercise.name
        if ex_name not in sets_by_exercise:
            sets_by_exercise[ex_name] = {
                'exercise': exercise_set.exercise,
                'sets': [],
                'total_volume': 0
            }
        sets_by_exercise[ex_name]['sets'].append(exercise_set)
        sets_by_exercise[ex_name]['total_volume'] += exercise_set.volume
    
    return render(request, 'web/workout/detail.html', {
        'session': session,
        'sets_by_exercise': sets_by_exercise
    })
