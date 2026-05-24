from django.utils.translation import gettext as _

def calculate_bmr_tdee(age, gender, height, weight, activity_level):
    """
    Calculates basal metabolic rate (BMR) and total daily energy expenditure (TDEE).
    
    Args:
        age (int): Age in years
        gender (str): Gender ('male' or 'female')
        height (int): Height in cm
        weight (int): Weight in kg
        activity_level (str): Activity level ('sedentary', 'moderate', 'active', 'elite')
    
    Returns:
        int: TDEE (Total Daily Energy Expenditure) in calories
    """
    # Mifflin-St Jeor Equation
    bmr = 10 * weight + 6.25 * height - 5 * age
    bmr += 5 if gender == 'male' else -161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'moderate': 1.55,
        'active': 1.725,
        'elite': 1.9
    }
    # Default to moderate if not found
    multiplier = activity_multipliers.get(activity_level, 1.55)
    tdee = bmr * multiplier
    return tdee

def calculate_macros(weight, target_calories):
    """
    Calculates macronutrient distribution (protein, carbs, fats).
    
    Args:
        weight (int): Weight in kg
        target_calories (int): Target daily calories
    
    Returns:
        dict: Macro distribution in grams
    """
    # Protein: 2g per kg of bodyweight (Standard for active individuals)
    protein_g = int(weight * 2)
    protein_cals = protein_g * 4
    
    # Remaining calories for Carbs and Fats
    remaining_cals = target_calories - protein_cals
    
    # Split remaining: 60% Carbs, 40% Fats
    carbs_cals = remaining_cals * 0.60
    fats_cals = remaining_cals * 0.40
    
    carbs_g = int(carbs_cals / 4)
    fats_g = int(fats_cals / 9)
    
    return {
        "protein": f"{protein_g}g",
        "carbs": f"{carbs_g}g",
        "fats": f"{fats_g}g"
    }

def get_meal_plan():
    """
    Generates a sample meal plan with recommendations.
    
    Returns:
        str: Formatted meal plan
    """
    return {
        "breakfast": _("Oatmeal, whey protein & berries"),
        "lunch": _("Chicken breast, quinoa, roasted vegetables"),
        "snack": _("Greek yogurt & almonds"),
        "dinner": _("Salmon fillet with sweet potato")
    }
