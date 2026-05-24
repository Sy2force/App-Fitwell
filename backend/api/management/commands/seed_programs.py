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
                'name': 'Weight Loss - 4 Weeks',
                'goal': 'weight_loss',
                'level': 'beginner',
                'duration': '4_weeks',
                'description_short': 'Cardio and full body program to lose weight healthily',
                'description_long': 'This program combines cardio and strength exercises to maximize calorie expenditure while preserving muscle mass. Ideal for starting sustainable weight loss.',
                'total_sessions': 12,
                'duration_weeks': 4,
                'nutrition_tips': 'Reduce refined sugars, increase protein intake, drink plenty of water. Eat vegetables with every meal.',
                'equipment_needed': 'No equipment needed. Just your body and motivation.',
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
                    name=f"Day {day_num} - {'Active Rest' if is_rest else 'Cardio + Strength'}",
                    description="30-minute session with warm-up, main workout and cool-down." if not is_rest else "Light rest day with walking or stretching.",
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
                            weight_note='Bodyweight'
                        )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program1.name}"))
        
        # Program 2: Muscle Gain (Strength)
        program2, created = Program.objects.update_or_create(
            slug='muscle-gain-8-weeks',
            defaults={
                'name': 'Muscle Gain - 8 Weeks',
                'goal': 'muscle_gain',
                'level': 'intermediate',
                'duration': '8_weeks',
                'description_short': 'Progressive strength program to gain strength and volume',
                'description_long': 'Structured 8-week program with progressive load increase. Focus on compound movements for maximum mass gain.',
                'total_sessions': 24,
                'duration_weeks': 8,
                'nutrition_tips': 'Increase calorie intake by 300-500 kcal. Prioritize protein (2g/kg body weight). Consume complex carbs before and after training.',
                'equipment_needed': 'Dumbbells or barbell, bench, bodyweight.',
                'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1600'
            }
        )
        
        if created:
            # Create days for program 2 (Push/Pull/Legs split)
            for day_num in range(1, 25):
                is_rest = day_num in [7, 14, 21]
                split_type = day_num % 3
                if split_type == 1:
                    name = "Push (Chest, Shoulders, Triceps)"
                    muscles = ['chest', 'shoulders', 'arms']
                elif split_type == 2:
                    name = "Pull (Back, Biceps)"
                    muscles = ['back', 'arms']
                else:
                    name = "Legs (Legs)"
                    muscles = ['legs']
                
                day = ProgramDay.objects.create(
                    program=program2,
                    day_number=day_num,
                    name=f"Day {day_num} - {name if not is_rest else 'Rest'}",
                    description="45-60 minute session with focus on intensity and progression." if not is_rest else "Full rest to allow muscle recovery.",
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
                            weight_note='Progressive'
                        )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program2.name}"))
        
        # Program 3: Mobility & Yoga
        program3, created = Program.objects.update_or_create(
            slug='mobility-yoga-7-days',
            defaults={
                'name': 'Mobility & Yoga - 7 Days',
                'goal': 'mobility',
                'level': 'beginner',
                'duration': '7_days',
                'description_short': 'Mobility and yoga program to improve flexibility and posture',
                'description_long': '7 days of mobility and yoga exercises to improve your posture, reduce tension and prevent injuries. Perfect for beginners or as active recovery.',
                'total_sessions': 7,
                'duration_weeks': 1,
                'nutrition_tips': 'Hydration essential for mobility. Magnesium and potassium to prevent cramps.',
                'equipment_needed': 'Yoga mat recommended, but not required.',
                'image': 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?q=80&w=1600'
            }
        )
        
        if created:
            for day_num in range(1, 8):
                day = ProgramDay.objects.create(
                    program=program3,
                    day_number=day_num,
                    name=f"Day {day_num} - Yoga Flow & Stretching",
                    description="20-minute session of yoga and dynamic stretching.",
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
                        reps='30-60 seconds',
                        rest_seconds=30,
                        weight_note='No weight'
                    )
        
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} program: {program3.name}"))
        
        self.stdout.write(self.style.SUCCESS('Programs seeded successfully!'))
