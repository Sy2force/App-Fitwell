from api.models import Badge, UserBadge, WorkoutSession, Comment

def check_and_award_badges(user):
    """
    Checks and automatically awards badges to a user.
    Returns the list of newly unlocked badges.
    """
    newly_unlocked = []
    
    # Get user stats
    if not hasattr(user, 'stats'):
        return newly_unlocked

    stats = user.stats
    workout_count = WorkoutSession.objects.filter(user=user, status='completed').count()
    total_volume = sum(s.total_volume for s in WorkoutSession.objects.filter(user=user, status='completed'))
    comment_count = Comment.objects.filter(author=user).count()
    plan_count = user.plans.count()
    
    # Get all badges
    all_badges = Badge.objects.all()
    
    # Get already unlocked badges
    unlocked_badge_ids = user.badges.values_list('badge_id', flat=True)
    
    for badge in all_badges:
        # Skip if already unlocked
        if badge.id in unlocked_badge_ids:
            continue
        
        # Check conditions
        should_unlock = False
        
        if badge.condition_type == 'workout_count':
            should_unlock = workout_count >= badge.condition_value
        elif badge.condition_type == 'total_volume':
            should_unlock = total_volume >= badge.condition_value
        elif badge.condition_type == 'current_streak':
            should_unlock = stats.current_streak >= badge.condition_value
        elif badge.condition_type == 'level':
            should_unlock = stats.level >= badge.condition_value
        elif badge.condition_type == 'plan_count':
            should_unlock = plan_count >= badge.condition_value
        elif badge.condition_type == 'comment_count':
            should_unlock = comment_count >= badge.condition_value
        elif badge.condition_type == 'account_created':
            should_unlock = True
        
        if should_unlock:
            # Award badge
            UserBadge.objects.create(user=user, badge=badge)
            # Award XP
            stats.add_xp(badge.xp_reward)
            newly_unlocked.append(badge)
    
    return newly_unlocked
