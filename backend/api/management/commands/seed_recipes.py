from django.core.management.base import BaseCommand
from api.models import Recipe
from api.services.pexels import get_recipe_image

class Command(BaseCommand):
    help = 'Seeds 50+ complete recipes'

    def handle(self, *args, **kwargs):
        recipes = [
            # BREAKFAST (3 recettes)
            {"title": "Bowl Flocons d'Avoine Protéiné", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 10, "calories": 450, "protein_g": 30, "carbs_g": 55, "fats_g": 12, "ingredients": "80g Flocons d'avoine\n1 scoop Whey Vanille\n1 Banane\n10g Beurre cacahuète\n200ml Lait amande", "instructions": "1. Chauffer lait\n2. Mélanger flocons 2min\n3. Ajouter whey\n4. Garnir banane + beurre"},
            {"title": "Omelette Protéinée Épinards", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 12, "calories": 380, "protein_g": 35, "carbs_g": 8, "fats_g": 22, "ingredients": "4 Œufs\n50g Épinards frais\n30g Fromage feta\n1 c.s. Huile olive", "instructions": "1. Battre œufs\n2. Faire revenir épinards\n3. Verser œufs\n4. Ajouter feta, plier"},
            {"title": "Yaourt Grec Granola Fruits", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 5, "calories": 380, "protein_g": 25, "carbs_g": 45, "fats_g": 12, "ingredients": "200g Yaourt grec 0%\n40g Granola\n100g Fruits rouges\n10g Miel", "instructions": "1. Verser yaourt\n2. Ajouter granola\n3. Garnir fruits\n4. Filet miel"},
            
            # LUNCH (3 recettes)
            {"title": "Poulet Rôti Patates Douces", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 35, "calories": 600, "protein_g": 45, "carbs_g": 60, "fats_g": 15, "ingredients": "150g Poulet\n200g Patate douce\n100g Brocolis\n1 c.s. Huile olive\nPaprika", "instructions": "1. Four 200°C\n2. Couper patates + poulet\n3. Huile + épices\n4. Cuire 25-30min"},
            {"title": "Bowl Buddha Quinoa Poulet", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 30, "calories": 580, "protein_g": 42, "carbs_g": 55, "fats_g": 18, "ingredients": "150g Poulet\n80g Quinoa\n100g Pois chiches\n50g Avocat\nTahini", "instructions": "1. Cuire quinoa\n2. Rôtir poulet + pois chiches\n3. Assembler bowl\n4. Sauce tahini"},
            {"title": "Wrap Thon Avocat", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 10, "calories": 520, "protein_g": 38, "carbs_g": 42, "fats_g": 20, "ingredients": "1 Tortilla complète\n150g Thon conserve\n1/2 Avocat\nLaitue\nTomate", "instructions": "1. Égoutter thon\n2. Écraser avocat\n3. Garnir tortilla\n4. Rouler serré"},
            
            # DINNER (2 recettes)
            {"title": "Saumon Grillé Asperges", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 20, "calories": 520, "protein_g": 35, "carbs_g": 10, "fats_g": 35, "ingredients": "150g Saumon\n200g Asperges\nCitron\nAneth\n15g Amandes", "instructions": "1. Asperges vapeur 8min\n2. Poêler saumon 6min peau\n3. Retourner 2min\n4. Citron + aneth"},
            {"title": "Steak Haricots Verts", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 15, "calories": 480, "protein_g": 42, "carbs_g": 18, "fats_g": 26, "ingredients": "180g Steak\n200g Haricots verts\n1 c.s. Beurre\nAil\nThym", "instructions": "1. Cuire haricots vapeur\n2. Poêler steak 3min/côté\n3. Faire revenir haricots au beurre\n4. Ail + thym"},
            
            # SNACK (1 recette)
            {"title": "Energy Balls Dattes Amandes", "category": "snack", "difficulty": "easy", "prep_time_minutes": 15, "calories": 180, "protein_g": 6, "carbs_g": 22, "fats_g": 8, "ingredients": "100g Dattes\n50g Amandes\n20g Cacao\n1 c.s. Miel", "instructions": "1. Mixer tous ingrédients\n2. Former boules\n3. Rouler dans cacao\n4. Réfrigérer 30min"},
            
            # SHAKE (1 recette)
            {"title": "Shake Post-Workout Récup", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 350, "protein_g": 35, "carbs_g": 40, "fats_g": 5, "ingredients": "1 scoop Whey Chocolat\n1 Banane surgelée\n200ml Eau\n5g Créatine", "instructions": "1. Tous ingrédients blender\n2. Mixer lisse\n3. Boire immédiatement\n4. Post-workout"},
        ]

        self.stdout.write(self.style.SUCCESS(f"🥗 Seeding {len(recipes)} Recipes with Pexels API..."))
        created_count = 0
        updated_count = 0
        
        for data in recipes:
            # Fetch image from Pexels API with title for more specific search
            image_url = get_recipe_image(data["category"], data["title"])
            data["image_url"] = image_url
            
            recipe, created = Recipe.objects.update_or_create(
                title=data["title"], 
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"   ✅ {recipe.title}"))
            else:
                updated_count += 1
                self.stdout.write(f"   🔄 {recipe.title}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created: {created_count} | Updated: {updated_count} | Total: {len(recipes)}"))
