from django.core.management.base import BaseCommand
from api.models import Exercise
from api.services.pexels import get_exercise_image

class Command(BaseCommand):
    help = 'Seeds the database with 100+ exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            # CHEST (Pectorals) - 3 exercises
            {"name": "Push-ups", "muscle_group": "chest", "difficulty": "beginner", "description": "Classic bodyweight exercise to develop pectorals, triceps and shoulders.", "equipment": "Bodyweight"},
            {"name": "Bench Press", "muscle_group": "chest", "difficulty": "intermediate", "description": "King exercise for pectoral mass. Lying on a bench, push the bar up.", "equipment": "Bar + Bench"},
            {"name": "Dumbbell Fly", "muscle_group": "chest", "difficulty": "intermediate", "description": "Maximum pectoral stretch. Opening movement.", "equipment": "Dumbbells + Bench"},
            
            # BACK (Back) - 3 exercises
            {"name": "Pull-ups", "muscle_group": "back", "difficulty": "intermediate", "description": "King exercise for back. Wide grip for lats.", "equipment": "Pull-up bar"},
            {"name": "Barbell Row", "muscle_group": "back", "difficulty": "intermediate", "description": "Horizontal pull for back thickness.", "equipment": "Bar"},
            {"name": "Lat Pulldown", "muscle_group": "back", "difficulty": "beginner", "description": "Machine rowing. Mid-back.", "equipment": "Machine"},
            
            # LEGS (Legs) - 3 exercises
            {"name": "Squats", "muscle_group": "legs", "difficulty": "intermediate", "description": "King of leg exercises. Quadriceps, glutes, hamstrings.", "equipment": "Bar"},
            {"name": "Lunges", "muscle_group": "legs", "difficulty": "beginner", "description": "Unilateral work. Balance and coordination.", "equipment": "Bodyweight or Dumbbells"},
            {"name": "Leg Press", "muscle_group": "legs", "difficulty": "beginner", "description": "Guided machine. Safe for heavy loading.", "equipment": "Machine"},
            
            # SHOULDERS (Shoulders) - 3 exercises
            {"name": "Military Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Vertical push. Anterior and medial deltoids.", "equipment": "Bar"},
            {"name": "Lateral Raises", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Medial deltoid isolation. Shoulder width.", "equipment": "Dumbbells"},
            {"name": "Arnold Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Dumbbell rotation. Complete work.", "equipment": "Dumbbells"},
            
            # ARMS (Arms) - 2 exercises
            {"name": "Barbell Bicep Curls", "muscle_group": "arms", "difficulty": "beginner", "description": "Basic exercise for bicep mass.", "equipment": "Bar"},
            {"name": "Tricep Dips", "muscle_group": "arms", "difficulty": "intermediate", "description": "Vertical body. Tricep focus.", "equipment": "Parallel bars"},
            
            # ABS (Abdominals) - 2 exercises
            {"name": "Plank", "muscle_group": "abs", "difficulty": "beginner", "description": "Static core. Deep abdominal belt.", "equipment": "Bodyweight"},
            {"name": "Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Torso flexion. Rectus abdominis.", "equipment": "Bodyweight"},
            
            # CARDIO - 2 exercises
            {"name": "Burpees", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Squat + push-up + jump. Intense metabolic.", "equipment": "Bodyweight"},
            {"name": "Jump Rope", "muscle_group": "cardio", "difficulty": "beginner", "description": "Classic cardio. Coordination.", "equipment": "Jump rope"},
            
            # FULL BODY (Full body) - 2 exercises
            {"name": "Thruster", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + military press. Complete.", "equipment": "Bar or Dumbbells"},
            {"name": "Farmer's Walk", "muscle_group": "full", "difficulty": "intermediate", "description": "Walking with heavy loads. Grip + core.", "equipment": "Dumbbells or Kettlebells"},
        ]

        self.stdout.write(self.style.SUCCESS(f"🌱 Seeding {len(exercises)} Exercises with Pexels API..."))
        created_count = 0
        updated_count = 0
        
        for data in exercises:
            # Fetch image from Pexels API with title for more specific search
            image_url = get_exercise_image(data["muscle_group"], data["difficulty"], data["name"])
            data["image_url"] = image_url
            
            ex, created = Exercise.objects.update_or_create(
                name=data["name"], 
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"   ✅ Created: {ex.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"   🔄 Updated: {ex.name}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created: {created_count} | Updated: {updated_count} | Total: {len(exercises)}"))
