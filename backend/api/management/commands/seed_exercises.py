from django.core.management.base import BaseCommand
from api.models import Exercise
from api.services.pexels import get_exercise_image

class Command(BaseCommand):
    help = 'Seeds the database with 100+ exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            # CHEST (Pectoraux) - 3 exercices
            {"name": "Pompes (Push-ups)", "muscle_group": "chest", "difficulty": "beginner", "description": "Exercice classique au poids du corps pour développer les pectoraux, triceps et épaules.", "equipment": "Poids du corps"},
            {"name": "Développé Couché (Bench Press)", "muscle_group": "chest", "difficulty": "intermediate", "description": "Exercice roi pour la masse pectorale. Allongé sur un banc, poussez la barre vers le haut.", "equipment": "Barre + Banc"},
            {"name": "Écarté Haltères", "muscle_group": "chest", "difficulty": "intermediate", "description": "Étirement maximal des pectoraux. Mouvement d'ouverture.", "equipment": "Haltères + Banc"},
            
            # BACK (Dos) - 3 exercices
            {"name": "Tractions (Pull-ups)", "muscle_group": "back", "difficulty": "intermediate", "description": "Exercice roi pour le dos. Prise large pour les dorsaux.", "equipment": "Barre de traction"},
            {"name": "Rowing Barre", "muscle_group": "back", "difficulty": "intermediate", "description": "Tirage horizontal pour l'épaisseur du dos.", "equipment": "Barre"},
            {"name": "Tirage Horizontal", "muscle_group": "back", "difficulty": "beginner", "description": "Rowing à la machine. Milieu du dos.", "equipment": "Machine"},
            
            # LEGS (Jambes) - 3 exercices
            {"name": "Squats", "muscle_group": "legs", "difficulty": "intermediate", "description": "Roi des exercices jambes. Quadriceps, fessiers, ischio.", "equipment": "Barre"},
            {"name": "Fentes (Lunges)", "muscle_group": "legs", "difficulty": "beginner", "description": "Travail unilatéral. Équilibre et coordination.", "equipment": "Poids du corps ou Haltères"},
            {"name": "Leg Press", "muscle_group": "legs", "difficulty": "beginner", "description": "Machine guidée. Sécuritaire pour charger lourd.", "equipment": "Machine"},
            
            # SHOULDERS (Épaules) - 3 exercices
            {"name": "Développé Militaire", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Poussée verticale. Deltoïdes antérieurs et moyens.", "equipment": "Barre"},
            {"name": "Élévations Latérales", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes moyens. Largeur d'épaules.", "equipment": "Haltères"},
            {"name": "Arnold Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Rotation des haltères. Travail complet.", "equipment": "Haltères"},
            
            # ARMS (Bras) - 2 exercices
            {"name": "Curls Biceps Barre", "muscle_group": "arms", "difficulty": "beginner", "description": "Exercice de base pour la masse des biceps.", "equipment": "Barre"},
            {"name": "Dips Triceps", "muscle_group": "arms", "difficulty": "intermediate", "description": "Corps vertical. Focus triceps.", "equipment": "Barres parallèles"},
            
            # ABS (Abdominaux) - 2 exercices
            {"name": "Planche (Plank)", "muscle_group": "abs", "difficulty": "beginner", "description": "Gainage statique. Sangle abdominale profonde.", "equipment": "Poids du corps"},
            {"name": "Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Flexion du buste. Grand droit.", "equipment": "Poids du corps"},
            
            # CARDIO - 2 exercices
            {"name": "Burpees", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Squat + pompe + saut. Métabolique intense.", "equipment": "Poids du corps"},
            {"name": "Jump Rope (Corde à sauter)", "muscle_group": "cardio", "difficulty": "beginner", "description": "Cardio classique. Coordination.", "equipment": "Corde à sauter"},
            
            # FULL BODY (Corps complet) - 2 exercices
            {"name": "Thruster", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + développé militaire. Complet.", "equipment": "Barre ou Haltères"},
            {"name": "Farmer's Walk", "muscle_group": "full", "difficulty": "intermediate", "description": "Marche avec charges lourdes. Grip + core.", "equipment": "Haltères ou Kettlebells"},
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
