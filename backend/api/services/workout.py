from django.utils.translation import gettext as _

def generate_split_training(goal, activity_level):
    """
    Generates a training program adapted to level and goal.
    
    Args:
        goal (str): Goal ('weight_loss', 'muscle_gain', 'maintenance')
        activity_level (str): Activity level
    
    Returns:
        str: Formatted training program
    """
    if activity_level in ['elite', 'active']:
        # PPL Split for active users
        return {
            'type': 'PPL',
            'frequency': '6x/week' if activity_level == 'elite' else '3x/week',
            'split': {
                'push': {
                    'focus': 'Chest, Shoulders, Triceps',
                    'exercises': ['Bench Press', 'Incline Press', 'Military Press', 'Lateral Raises', 'Tricep Dips'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                },
                'pull': {
                    'focus': 'Back, Biceps',
                    'exercises': ['Pull-ups', 'Barbell Row', 'Lat Pulldown', 'Dumbbell Row', 'Bicep Curls'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                },
                'legs': {
                    'focus': 'Legs, Abs',
                    'exercises': ['Squats', 'Deadlift', 'Leg Press', 'Lunges', 'Plank'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                }
            }
        }
    else:
        # Full Body for beginners/moderate
        return {
            'type': 'Full Body',
            'frequency': '3x/week',
            'exercises': ['Squats', 'Bench Press', 'Barbell Row', 'Military Press', 'Pull-ups', 'Plank'],
            'sets': '3-4 sets per exercise',
            'reps': '10-12 reps' if goal == 'muscle_gain' else '12-15 reps',
            'rest': '90-120 seconds'
        }

def get_workout_schedule(activity_level):
    """
    Determines recommended training frequency.
    
    Args:
        activity_level (str): Activity level
    
    Returns:
        str: Weekly training schedule
    """
    schedule = _("4 days/week - upper/lower split")
    if activity_level in ['active', 'elite']:
        schedule = _("6 days/week - PPL Split (Push/Pull/Legs)")
    return schedule

def get_base_exercises():
    """
    Returns the list of recommended base exercises.
    
    Returns:
        str: List of fundamental exercises
    """
    return [
        _("Compound movements (squat, deadlift, bench press)"),
        _("Accessory work (dumbbells, pulleys)"),
        _("Mobility (10 min before session)"),
        _("Zone 2 cardio (2x 30min)")
    ]
