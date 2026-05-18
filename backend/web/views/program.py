from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models import Program, ProgramDay, ProgramExercise, UserProgramProgress, User
from django.utils import timezone


def program_list(request):
    """
    Liste de tous les programmes d'entraînement.
    Filtres par objectif, niveau, durée.
    """
    programs = Program.objects.all()
    
    # Filtres
    goal_filter = request.GET.get('goal')
    level_filter = request.GET.get('level')
    duration_filter = request.GET.get('duration')
    
    if goal_filter:
        programs = programs.filter(goal=goal_filter)
    if level_filter:
        programs = programs.filter(level=level_filter)
    if duration_filter:
        programs = programs.filter(duration=duration_filter)
    
    # Vérifier si l'utilisateur a commencé un programme
    user_progress = None
    if request.user.is_authenticated:
        user_progress = UserProgramProgress.objects.filter(
            user=request.user,
            status='in_progress'
        ).first()
    
    context = {
        'programs': programs,
        'goal_filter': goal_filter,
        'level_filter': level_filter,
        'duration_filter': duration_filter,
        'user_progress': user_progress,
    }
    return render(request, 'web/programs_list.html', context)


def program_detail(request, slug):
    """
    Détail d'un programme avec ses jours et exercices.
    """
    program = get_object_or_404(Program, slug=slug)
    days = program.days.all().prefetch_related('exercises__exercise')
    
    # Vérifier la progression de l'utilisateur
    user_progress = None
    if request.user.is_authenticated:
        user_progress, created = UserProgramProgress.objects.get_or_create(
            user=request.user,
            program=program,
            defaults={'status': 'not_started'}
        )
    
    context = {
        'program': program,
        'days': days,
        'user_progress': user_progress,
    }
    return render(request, 'web/program_detail.html', context)


@login_required
def start_program(request, program_id):
    """
    Démarrer un programme pour l'utilisateur.
    """
    program = get_object_or_404(Program, id=program_id)
    user_progress, created = UserProgramProgress.objects.get_or_create(
        user=request.user,
        program=program,
        defaults={'status': 'not_started'}
    )
    
    if user_progress.status == 'not_started':
        user_progress.status = 'in_progress'
        user_progress.started_at = timezone.now()
        user_progress.current_day = 1
        user_progress.save()
    
    return redirect('program_detail', slug=program.slug)


@login_required
def complete_program_day(request, program_id, day_number):
    """
    Marquer un jour de programme comme complété.
    """
    program = get_object_or_404(Program, id=program_id)
    user_progress = get_object_or_404(
        UserProgramProgress,
        user=request.user,
        program=program
    )
    
    # Ajouter le jour aux jours complétés
    if str(day_number) not in user_progress.days_completed:
        user_progress.days_completed.append(str(day_number))
        user_progress.current_day = min(day_number + 1, program.total_sessions)
        
        # Vérifier si le programme est terminé
        if len(user_progress.days_completed) >= program.total_sessions:
            user_progress.status = 'completed'
            user_progress.completed_at = timezone.now()
        
        user_progress.save()
    
    return redirect('program_detail', slug=program.slug)
