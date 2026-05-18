from django.core.management.base import BaseCommand
from api.models import Program, ProgramDay, ProgramExercise, Exercise


class Command(BaseCommand):
    help = 'Seed the database with sample training programs'

    def handle(self, *args, **options):
        self.stdout.write('Seeding programs...')
        
        # Get exercises for programs
        exercises = list(Exercise.objects.all())
        
        if len(exercises) < 10:
            self.stdout.write(self.style.WARNING('Not enough exercises in database. Run seed_exercises first.'))
            return
        
        # Program 1: Weight Loss (Cardio + Full Body)
        program1, created = Program.objects.update_or_create(
            slug='weight-loss-4-weeks',
            defaults={
                'name': 'Perte de Poids - 4 Semaines',
                'goal': 'weight_loss',
                'level': 'beginner',
                'duration': '4_weeks',
                'description_short': 'Programme cardio et corps complet pour perdre du poids sainement',
                'description_long': 'Ce programme combine des exercices cardio et de renforcement musculaire pour maximiser la dépense calorique tout en préservant la masse musculaire. Idéal pour débuter une perte de poids durable.',
                'total_sessions': 12,
                'duration_weeks': 4,
                'nutrition_tips': 'Réduis les sucres raffinés, augmente ton apport en protéines, bois beaucoup d\'eau. Mange des légumes à chaque repas.',
                'equipment_needed': 'Aucun équipement nécessaire. Juste ton corps et de la motivation.',
                'image': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?q=80&w=1600'
            }
        )
        
        if created:
            # Create days for program 1
            for day_num in range(1, 13):
                is_rest = day_num in [4, 8]
                day = ProgramDay.objects.create(
                    program=program1,
                    day_number=day_num,
                    name=f"Jour {day_num} - {'Repos Actif' if is_rest else 'Cardio + Renforcement'}",
                    description="Séance de 30 minutes avec échauffement, entraînement principal et retour au calme." if not is_rest else "Jour de repos léger avec marche ou étirements.",
                    is_rest_day=is_rest,
                    estimated_duration_minutes=30 if not is_rest else 15
                )
                
                if not is_rest:
                    # Add exercises to the day
                    chest_exercises = [e for e in exercises if e.muscle_group == 'chest'][:2]
                    leg_exercises = [e for e in exercises if e.muscle_group == 'legs'][:2]
                    cardio_exercises = [e for e in exercises if e.muscle_group == 'cardio'][:2]
                    
                    day_exercises = (chest_exercises + leg_exercises + cardio_exercises)[:4]
                    for idx, exercise in enumerate(day_exercises, 1):
                        ProgramExercise.objects.create(
                            program_day=day,
                            exercise=exercise,
                            order=idx,
                            sets=3,
                            reps='12-15',
                            rest_seconds=60,
                            weight_note='Poids du corps'
                        )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program1.name}"))
        
        # Program 2: Muscle Gain (Strength)
        program2, created = Program.objects.update_or_create(
            slug='muscle-gain-8-weeks',
            defaults={
                'name': 'Prise de Masse - 8 Semaines',
                'goal': 'muscle_gain',
                'level': 'intermediate',
                'duration': '8_weeks',
                'description_short': 'Programme musculation progressive pour gagner en force et en volume',
                'description_long': 'Programme structuré en 8 semaines avec une progression progressive des charges. Focus sur les mouvements composants pour une prise de masse maximale.',
                'total_sessions': 24,
                'duration_weeks': 8,
                'nutrition_tips': 'Augmente ton apport calorique de 300-500 kcal. Priorité aux protéines (2g/kg de poids corporel). Consomme des glucides complexes avant et après l\'entraînement.',
                'equipment_needed': 'Haltères ou barbell, banc, poids de corps.',
                'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1600'
            }
        )
        
        if created:
            # Create days for program 2 (Push/Pull/Legs split)
            for day_num in range(1, 25):
                is_rest = day_num in [7, 14, 21]
                split_type = day_num % 3
                if split_type == 1:
                    name = "Push (Pectoraux, Épaules, Triceps)"
                    muscles = ['chest', 'shoulders', 'arms']
                elif split_type == 2:
                    name = "Pull (Dos, Biceps)"
                    muscles = ['back', 'arms']
                else:
                    name = "Legs (Jambes)"
                    muscles = ['legs']
                
                day = ProgramDay.objects.create(
                    program=program2,
                    day_number=day_num,
                    name=f"Jour {day_num} - {name if not is_rest else 'Repos'}",
                    description="Séance de 45-60 minutes avec focus sur l\'intensité et la progression." if not is_rest else "Repos complet pour permettre la récupération musculaire.",
                    is_rest_day=is_rest,
                    estimated_duration_minutes=60 if not is_rest else 0
                )
                
                if not is_rest:
                    # Add exercises based on split
                    day_exercises = []
                    for muscle in muscles:
                        day_exercises.extend([e for e in exercises if e.muscle_group == muscle][:2])
                    
                    for idx, exercise in enumerate(day_exercises[:5], 1):
                        ProgramExercise.objects.create(
                            program_day=day,
                            exercise=exercise,
                            order=idx,
                            sets=4,
                            reps='8-12',
                            rest_seconds=90,
                            weight_note='Progressif'
                        )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program2.name}"))
        
        # Program 3: Mobility & Yoga
        program3, created = Program.objects.update_or_create(
            slug='mobility-yoga-7-days',
            defaults={
                'name': 'Mobilité & Yoga - 7 Jours',
                'goal': 'mobility',
                'level': 'beginner',
                'duration': '7_days',
                'description_short': 'Programme de mobilité et yoga pour améliorer souplesse et posture',
                'description_long': '7 jours d\'exercices de mobilité et de yoga pour améliorer ta posture, réduire les tensions et prévenir les blessures. Parfait pour les débutants ou comme récupération active.',
                'total_sessions': 7,
                'duration_weeks': 1,
                'nutrition_tips': 'Hydratation essentielle pour la mobilité. Magnésium et potassium pour prévenir les crampes.',
                'equipment_needed': 'Tapis de yoga recommandé, mais pas obligatoire.',
                'image': 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?q=80&w=1600'
            }
        )
        
        if created:
            for day_num in range(1, 8):
                day = ProgramDay.objects.create(
                    program=program3,
                    day_number=day_num,
                    name=f"Jour {day_num} - Flow Yoga & Étirements",
                    description="Séance de 20 minutes de yoga et d'étirements dynamiques.",
                    is_rest_day=False,
                    estimated_duration_minutes=20
                )
                
                # Add flexibility exercises
                full_body = [e for e in exercises if e.muscle_group == 'full'][:3]
                for idx, exercise in enumerate(full_body, 1):
                    ProgramExercise.objects.create(
                        program_day=day,
                        exercise=exercise,
                        order=idx,
                        sets=2,
                        reps='30-60 secondes',
                        rest_seconds=30,
                        weight_note='Sans poids'
                    )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program3.name}"))
        
        self.stdout.write(self.style.SUCCESS('Programs seeded successfully!'))
