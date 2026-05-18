from django.core.management.base import BaseCommand
from api.models import Exercise
from api.services.pexels import get_exercise_image

class Command(BaseCommand):
    help = 'Seeds the database with 100+ exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            # CHEST (Pectoraux) - 15 exercices
            {"name": "Pompes (Push-ups)", "muscle_group": "chest", "difficulty": "beginner", "description": "Exercice classique au poids du corps pour développer les pectoraux, triceps et épaules.", "equipment": "Poids du corps"},
            {"name": "Développé Couché (Bench Press)", "muscle_group": "chest", "difficulty": "intermediate", "description": "Exercice roi pour la masse pectorale. Allongé sur un banc, poussez la barre vers le haut.", "equipment": "Barre + Banc"},
            {"name": "Développé Incliné", "muscle_group": "chest", "difficulty": "intermediate", "description": "Cible le haut des pectoraux. Banc incliné à 30-45 degrés.", "equipment": "Haltères + Banc"},
            {"name": "Développé Décliné", "muscle_group": "chest", "difficulty": "intermediate", "description": "Focus sur le bas des pectoraux. Banc décliné.", "equipment": "Barre + Banc"},
            {"name": "Écarté Haltères", "muscle_group": "chest", "difficulty": "intermediate", "description": "Étirement maximal des pectoraux. Mouvement d'ouverture.", "equipment": "Haltères + Banc"},
            {"name": "Dips Pectoraux", "muscle_group": "chest", "difficulty": "intermediate", "description": "Penchez-vous en avant pour cibler les pectoraux.", "equipment": "Barres parallèles"},
            {"name": "Pompes Diamant", "muscle_group": "chest", "difficulty": "intermediate", "description": "Mains rapprochées en forme de diamant. Focus triceps et centre pectoraux.", "equipment": "Poids du corps"},
            {"name": "Pompes Déclinées", "muscle_group": "chest", "difficulty": "intermediate", "description": "Pieds surélevés pour augmenter l'intensité.", "equipment": "Poids du corps + Banc"},
            {"name": "Cable Crossover", "muscle_group": "chest", "difficulty": "intermediate", "description": "Croisement de câbles pour une contraction maximale.", "equipment": "Machine à câbles"},
            {"name": "Pec Deck (Butterfly)", "muscle_group": "chest", "difficulty": "beginner", "description": "Machine guidée pour isoler les pectoraux.", "equipment": "Machine"},
            {"name": "Développé Haltères", "muscle_group": "chest", "difficulty": "intermediate", "description": "Plus grande amplitude que la barre. Meilleur étirement.", "equipment": "Haltères + Banc"},
            {"name": "Pompes Pliométriques", "muscle_group": "chest", "difficulty": "advanced", "description": "Pompes explosives avec décollement des mains. Puissance.", "equipment": "Poids du corps"},
            {"name": "Pullover Haltère", "muscle_group": "chest", "difficulty": "intermediate", "description": "Étirement de la cage thoracique. Travaille aussi le dos.", "equipment": "Haltère + Banc"},
            {"name": "Pompes Archer", "muscle_group": "chest", "difficulty": "advanced", "description": "Pompes unilatérales. Un bras travaille plus que l'autre.", "equipment": "Poids du corps"},
            {"name": "Landmine Press", "muscle_group": "chest", "difficulty": "intermediate", "description": "Poussée avec barre en landmine. Angle unique.", "equipment": "Barre + Landmine"},
            
            # BACK (Dos) - 15 exercices
            {"name": "Tractions (Pull-ups)", "muscle_group": "back", "difficulty": "intermediate", "description": "Exercice roi pour le dos. Prise large pour les dorsaux.", "equipment": "Barre de traction"},
            {"name": "Soulevé de Terre", "muscle_group": "back", "difficulty": "advanced", "description": "Roi des exercices. Toute la chaîne postérieure.", "equipment": "Barre"},
            {"name": "Rowing Barre", "muscle_group": "back", "difficulty": "intermediate", "description": "Tirage horizontal pour l'épaisseur du dos.", "equipment": "Barre"},
            {"name": "Rowing Haltère", "muscle_group": "back", "difficulty": "intermediate", "description": "Tirage unilatéral. Corrige les déséquilibres.", "equipment": "Haltère + Banc"},
            {"name": "Tirage Vertical", "muscle_group": "back", "difficulty": "beginner", "description": "Alternative aux tractions. Machine guidée.", "equipment": "Machine"},
            {"name": "Tirage Horizontal", "muscle_group": "back", "difficulty": "beginner", "description": "Rowing à la machine. Milieu du dos.", "equipment": "Machine"},
            {"name": "Tractions Supination", "muscle_group": "back", "difficulty": "intermediate", "description": "Paumes vers soi. Plus de biceps.", "equipment": "Barre de traction"},
            {"name": "Face Pull", "muscle_group": "back", "difficulty": "beginner", "description": "Tirage vers le visage. Arrière d'épaules et trapèzes.", "equipment": "Câble"},
            {"name": "Shrugs (Haussements)", "muscle_group": "back", "difficulty": "beginner", "description": "Isolation des trapèzes supérieurs.", "equipment": "Haltères ou Barre"},
            {"name": "Soulevé de Terre Roumain", "muscle_group": "back", "difficulty": "intermediate", "description": "Variante jambes tendues. Focus ischio-jambiers.", "equipment": "Barre"},
            {"name": "T-Bar Row", "muscle_group": "back", "difficulty": "intermediate", "description": "Rowing avec barre en T. Épaisseur du dos.", "equipment": "Barre + Landmine"},
            {"name": "Pullover Câble", "muscle_group": "back", "difficulty": "intermediate", "description": "Extension des bras vers le bas. Dorsaux.", "equipment": "Câble"},
            {"name": "Good Morning", "muscle_group": "back", "difficulty": "intermediate", "description": "Flexion du buste. Lombaires et ischio-jambiers.", "equipment": "Barre"},
            {"name": "Hyperextensions", "muscle_group": "back", "difficulty": "beginner", "description": "Renforcement des lombaires. Banc à 45°.", "equipment": "Banc à lombaires"},
            {"name": "Seal Row", "muscle_group": "back", "difficulty": "intermediate", "description": "Rowing allongé sur banc. Élimine la triche.", "equipment": "Haltères + Banc"},
            
            # LEGS (Jambes) - 15 exercices
            {"name": "Squats", "muscle_group": "legs", "difficulty": "intermediate", "description": "Roi des exercices jambes. Quadriceps, fessiers, ischio.", "equipment": "Barre"},
            {"name": "Squats Avant", "muscle_group": "legs", "difficulty": "advanced", "description": "Barre devant. Plus de quadriceps, moins de dos.", "equipment": "Barre"},
            {"name": "Fentes (Lunges)", "muscle_group": "legs", "difficulty": "beginner", "description": "Travail unilatéral. Équilibre et coordination.", "equipment": "Poids du corps ou Haltères"},
            {"name": "Leg Press", "muscle_group": "legs", "difficulty": "beginner", "description": "Machine guidée. Sécuritaire pour charger lourd.", "equipment": "Machine"},
            {"name": "Leg Extension", "muscle_group": "legs", "difficulty": "beginner", "description": "Isolation des quadriceps. Finition.", "equipment": "Machine"},
            {"name": "Leg Curl", "muscle_group": "legs", "difficulty": "beginner", "description": "Isolation des ischio-jambiers.", "equipment": "Machine"},
            {"name": "Bulgarian Split Squat", "muscle_group": "legs", "difficulty": "intermediate", "description": "Fente arrière pied surélevé. Intense.", "equipment": "Haltères + Banc"},
            {"name": "Hack Squat", "muscle_group": "legs", "difficulty": "intermediate", "description": "Machine à squat inclinée. Quadriceps.", "equipment": "Machine"},
            {"name": "Goblet Squat", "muscle_group": "legs", "difficulty": "beginner", "description": "Squat avec haltère ou kettlebell devant.", "equipment": "Haltère"},
            {"name": "Step-ups", "muscle_group": "legs", "difficulty": "beginner", "description": "Montées sur banc. Fessiers et quadriceps.", "equipment": "Banc + Haltères"},
            {"name": "Sissy Squat", "muscle_group": "legs", "difficulty": "advanced", "description": "Squat penché en arrière. Quadriceps intense.", "equipment": "Poids du corps"},
            {"name": "Pistol Squat", "muscle_group": "legs", "difficulty": "advanced", "description": "Squat sur une jambe. Force et équilibre.", "equipment": "Poids du corps"},
            {"name": "Nordic Curl", "muscle_group": "legs", "difficulty": "advanced", "description": "Flexion ischio-jambiers assistée. Très intense.", "equipment": "Poids du corps"},
            {"name": "Calf Raises (Mollets)", "muscle_group": "legs", "difficulty": "beginner", "description": "Élévations sur pointes de pieds. Mollets.", "equipment": "Poids du corps ou Machine"},
            {"name": "Box Jumps", "muscle_group": "legs", "difficulty": "intermediate", "description": "Sauts sur boîte. Puissance explosive.", "equipment": "Boîte pliométrique"},
            
            # SHOULDERS (Épaules) - 12 exercices
            {"name": "Développé Militaire", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Poussée verticale. Deltoïdes antérieurs et moyens.", "equipment": "Barre"},
            {"name": "Développé Haltères Assis", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Plus grande amplitude que la barre.", "equipment": "Haltères + Banc"},
            {"name": "Élévations Latérales", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes moyens. Largeur d'épaules.", "equipment": "Haltères"},
            {"name": "Élévations Frontales", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes antérieurs.", "equipment": "Haltères ou Barre"},
            {"name": "Oiseau (Rear Delt Fly)", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes postérieurs. Penché en avant.", "equipment": "Haltères"},
            {"name": "Arnold Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Rotation des haltères. Travail complet.", "equipment": "Haltères"},
            {"name": "Upright Row", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Tirage vertical. Deltoïdes et trapèzes.", "equipment": "Barre ou Haltères"},
            {"name": "Pike Push-ups", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Pompes en V inversé. Poids du corps.", "equipment": "Poids du corps"},
            {"name": "Handstand Push-ups", "muscle_group": "shoulders", "difficulty": "advanced", "description": "Pompes en équilibre sur les mains. Très difficile.", "equipment": "Poids du corps"},
            {"name": "Cable Lateral Raise", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Élévations latérales au câble. Tension constante.", "equipment": "Câble"},
            {"name": "Bradford Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Développé avant/arrière alterné. Tension continue.", "equipment": "Barre"},
            {"name": "Lu Raise", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Élévation en arc de cercle. Deltoïdes complets.", "equipment": "Haltères"},
            
            # ARMS (Bras) - 12 exercices
            {"name": "Curls Biceps Barre", "muscle_group": "arms", "difficulty": "beginner", "description": "Exercice de base pour la masse des biceps.", "equipment": "Barre"},
            {"name": "Curls Haltères", "muscle_group": "arms", "difficulty": "beginner", "description": "Flexion alternée ou simultanée.", "equipment": "Haltères"},
            {"name": "Curls Marteau", "muscle_group": "arms", "difficulty": "beginner", "description": "Prise neutre. Brachial et avant-bras.", "equipment": "Haltères"},
            {"name": "Curls Pupitre", "muscle_group": "arms", "difficulty": "intermediate", "description": "Bras calés sur pupitre. Isolation stricte.", "equipment": "Haltère + Pupitre"},
            {"name": "Dips Triceps", "muscle_group": "arms", "difficulty": "intermediate", "description": "Corps vertical. Focus triceps.", "equipment": "Barres parallèles"},
            {"name": "Extensions Triceps", "muscle_group": "arms", "difficulty": "beginner", "description": "Bras au-dessus de la tête. Isolation longue portion.", "equipment": "Haltère"},
            {"name": "Kickback Triceps", "muscle_group": "arms", "difficulty": "beginner", "description": "Extension arrière. Finition triceps.", "equipment": "Haltères"},
            {"name": "Barre au Front", "muscle_group": "arms", "difficulty": "intermediate", "description": "Skull crushers. Triceps complets.", "equipment": "Barre + Banc"},
            {"name": "Curls Concentration", "muscle_group": "arms", "difficulty": "beginner", "description": "Assis, coude calé sur cuisse. Pic de contraction.", "equipment": "Haltère"},
            {"name": "Close Grip Bench", "muscle_group": "arms", "difficulty": "intermediate", "description": "Développé couché prise serrée. Triceps.", "equipment": "Barre + Banc"},
            {"name": "Cable Pushdown", "muscle_group": "arms", "difficulty": "beginner", "description": "Extension triceps au câble. Tension constante.", "equipment": "Câble"},
            {"name": "21s Biceps", "muscle_group": "arms", "difficulty": "intermediate", "description": "7 reps bas + 7 reps haut + 7 reps complètes. Congestion.", "equipment": "Barre"},
            
            # ABS (Abdominaux) - 12 exercices
            {"name": "Planche (Plank)", "muscle_group": "abs", "difficulty": "beginner", "description": "Gainage statique. Sangle abdominale profonde.", "equipment": "Poids du corps"},
            {"name": "Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Flexion du buste. Grand droit.", "equipment": "Poids du corps"},
            {"name": "Relevé de Jambes", "muscle_group": "abs", "difficulty": "intermediate", "description": "Bas des abdominaux. Allongé ou suspendu.", "equipment": "Poids du corps"},
            {"name": "Russian Twist", "muscle_group": "abs", "difficulty": "intermediate", "description": "Rotation du buste. Obliques.", "equipment": "Poids du corps ou Médecine ball"},
            {"name": "Mountain Climbers", "muscle_group": "abs", "difficulty": "intermediate", "description": "Genoux vers poitrine alternés. Cardio + abs.", "equipment": "Poids du corps"},
            {"name": "Ab Wheel Rollout", "muscle_group": "abs", "difficulty": "advanced", "description": "Roulette abdominale. Très intense.", "equipment": "Ab wheel"},
            {"name": "Planche Latérale", "muscle_group": "abs", "difficulty": "intermediate", "description": "Gainage sur le côté. Obliques.", "equipment": "Poids du corps"},
            {"name": "Bicycle Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Coude vers genou opposé. Rotation.", "equipment": "Poids du corps"},
            {"name": "V-Ups", "muscle_group": "abs", "difficulty": "intermediate", "description": "Toucher les pieds en V. Complet.", "equipment": "Poids du corps"},
            {"name": "Dragon Flag", "muscle_group": "abs", "difficulty": "advanced", "description": "Corps rigide suspendu. Très difficile.", "equipment": "Banc"},
            {"name": "Hollow Hold", "muscle_group": "abs", "difficulty": "intermediate", "description": "Position creuse maintenue. Gainage dynamique.", "equipment": "Poids du corps"},
            {"name": "Cable Crunch", "muscle_group": "abs", "difficulty": "intermediate", "description": "Crunch au câble. Résistance progressive.", "equipment": "Câble"},
            
            # CARDIO - 10 exercices
            {"name": "Burpees", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Squat + pompe + saut. Métabolique intense.", "equipment": "Poids du corps"},
            {"name": "Jump Rope (Corde à sauter)", "muscle_group": "cardio", "difficulty": "beginner", "description": "Cardio classique. Coordination.", "equipment": "Corde à sauter"},
            {"name": "Sprints", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Course à vitesse maximale. Explosivité.", "equipment": "Espace"},
            {"name": "Battle Ropes", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Ondes avec cordes lourdes. Cardio + bras.", "equipment": "Battle ropes"},
            {"name": "Rowing Machine", "muscle_group": "cardio", "difficulty": "beginner", "description": "Rameur. Cardio + dos.", "equipment": "Rameur"},
            {"name": "Assault Bike", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Vélo avec bras. Très intense.", "equipment": "Assault bike"},
            {"name": "High Knees", "muscle_group": "cardio", "difficulty": "beginner", "description": "Genoux hauts sur place. Cardio rapide.", "equipment": "Poids du corps"},
            {"name": "Jumping Jacks", "muscle_group": "cardio", "difficulty": "beginner", "description": "Échauffement classique. Cardio léger.", "equipment": "Poids du corps"},
            {"name": "Kettlebell Swings", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Balancement explosif. Cardio + postérieur.", "equipment": "Kettlebell"},
            {"name": "Sled Push", "muscle_group": "cardio", "difficulty": "advanced", "description": "Poussée de traîneau. Force + cardio.", "equipment": "Traîneau"},
            
            # FULL BODY (Corps complet) - 10 exercices
            {"name": "Thruster", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + développé militaire. Complet.", "equipment": "Barre ou Haltères"},
            {"name": "Clean & Press", "muscle_group": "full", "difficulty": "advanced", "description": "Épaulé + développé. Olympique.", "equipment": "Barre"},
            {"name": "Turkish Get-Up", "muscle_group": "full", "difficulty": "advanced", "description": "Se lever avec poids au-dessus de la tête. Stabilité.", "equipment": "Kettlebell"},
            {"name": "Man Makers", "muscle_group": "full", "difficulty": "advanced", "description": "Burpee + rowing + clean. Très complet.", "equipment": "Haltères"},
            {"name": "Bear Crawl", "muscle_group": "full", "difficulty": "intermediate", "description": "Marche à quatre pattes. Coordination.", "equipment": "Poids du corps"},
            {"name": "Farmer's Walk", "muscle_group": "full", "difficulty": "intermediate", "description": "Marche avec charges lourdes. Grip + core.", "equipment": "Haltères ou Kettlebells"},
            {"name": "Wall Balls", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + lancer de ballon. Explosif.", "equipment": "Médecine ball"},
            {"name": "Snatch (Arraché)", "muscle_group": "full", "difficulty": "advanced", "description": "Mouvement olympique. Puissance totale.", "equipment": "Barre"},
            {"name": "Clean (Épaulé)", "muscle_group": "full", "difficulty": "advanced", "description": "Barre du sol aux épaules. Explosif.", "equipment": "Barre"},
            {"name": "Devil Press", "muscle_group": "full", "difficulty": "advanced", "description": "Burpee + snatch haltères. Très intense.", "equipment": "Haltères"},
        ]

        self.stdout.write(self.style.SUCCESS(f"🌱 Seeding {len(exercises)} Exercises with Pexels API..."))
        created_count = 0
        updated_count = 0
        
        for data in exercises:
            # Fetch image from Pexels API
            image_url = get_exercise_image(data["muscle_group"], data["difficulty"])
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
