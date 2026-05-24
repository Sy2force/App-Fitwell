from django.utils.translation import gettext as _

def calculate_health_score(height, weight, activity_level):
    """
    Calculates overall health score and provides analysis.
    """
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    bmi_score = 0
    message = ""
    
    # BMI Scoring
    if 18.5 <= bmi <= 24.9:
        bmi_score = 90
        message = _("Your biometric profile is excellent. Maintain this foundation.")
    elif 25 <= bmi <= 29.9:
        bmi_score = 75
        message = _("Slight overweight detected. The plan includes a moderate calorie deficit.")
    elif bmi < 18.5:
        bmi_score = 70
        message = _("Low body mass index. Focus on hypertrophy and calorie surplus.")
    else:
        bmi_score = 60
        message = _("Metabolic optimization required. Priority to non-sport activity (NEAT).")

    # Activity Adjustment
    activity_bonus = {
        'sedentary': 0,
        'moderate': 5,
        'active': 10,
        'elite': 15
    }.get(activity_level, 5)

    health_score = int((bmi_score + 70 + activity_bonus) / 2)
    health_score = min(99, max(40, health_score)) # Clamp between 40 and 99

    return {
        "score": health_score,
        "message": message,
        "bmi": round(bmi, 1),
        "breakdown": {
            "fitness": 60 + (activity_bonus * 2),
            "recovery": 85 - activity_bonus,
            "lifestyle": 70 + activity_bonus,
            "consistency": 90
        }
    }
