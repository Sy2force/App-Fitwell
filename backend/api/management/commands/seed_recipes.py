from django.core.management.base import BaseCommand
from api.models import Recipe
from api.services.pexels import get_recipe_image

class Command(BaseCommand):
    help = 'Seeds 50+ complete recipes'

    def handle(self, *args, **kwargs):
        recipes = [
            # BREAKFAST (3 recipes)
            {"title": "Protein Oatmeal Bowl", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 10, "calories": 450, "protein_g": 30, "carbs_g": 55, "fats_g": 12, "ingredients": "80g Oats\n1 scoop Vanilla Whey\n1 Banana\n10g Peanut Butter\n200ml Almond milk", "instructions": "1. Heat milk\n2. Mix oats 2min\n3. Add whey\n4. Top with banana + butter"},
            {"title": "Spinach Protein Omelette", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 12, "calories": 380, "protein_g": 35, "carbs_g": 8, "fats_g": 22, "ingredients": "4 Eggs\n50g Fresh Spinach\n30g Feta cheese\n1 tbsp Olive oil", "instructions": "1. Beat eggs\n2. Sauté spinach\n3. Pour eggs\n4. Add feta, fold"},
            {"title": "Greek Yogurt Granola Fruit", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 5, "calories": 380, "protein_g": 25, "carbs_g": 45, "fats_g": 12, "ingredients": "200g Greek yogurt 0%\n40g Granola\n100g Berries\n10g Honey", "instructions": "1. Pour yogurt\n2. Add granola\n3. Top with fruit\n4. Drizzle honey"},
            
            # LUNCH (3 recipes)
            {"title": "Roasted Chicken Sweet Potato", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 35, "calories": 600, "protein_g": 45, "carbs_g": 60, "fats_g": 15, "ingredients": "150g Chicken\n200g Sweet potato\n100g Broccoli\n1 tbsp Olive oil\nPaprika", "instructions": "1. Oven 200°C\n2. Cut potato + chicken\n3. Oil + spices\n4. Bake 25-30min"},
            {"title": "Quinoa Chicken Buddha Bowl", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 30, "calories": 580, "protein_g": 42, "carbs_g": 55, "fats_g": 18, "ingredients": "150g Chicken\n80g Quinoa\n100g Chickpeas\n50g Avocado\nTahini", "instructions": "1. Cook quinoa\n2. Roast chicken + chickpeas\n3. Assemble bowl\n4. Tahini sauce"},
            {"title": "Tuna Avocado Wrap", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 10, "calories": 520, "protein_g": 38, "carbs_g": 42, "fats_g": 20, "ingredients": "1 Whole wheat tortilla\n150g Canned tuna\n1/2 Avocado\nLettuce\nTomato", "instructions": "1. Drain tuna\n2. Mash avocado\n3. Fill tortilla\n4. Roll tight"},
            
            # DINNER (2 recipes)
            {"title": "Grilled Salmon Asparagus", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 20, "calories": 520, "protein_g": 35, "carbs_g": 10, "fats_g": 35, "ingredients": "150g Salmon\n200g Asparagus\nLemon\nDill\n15g Almonds", "instructions": "1. Steam asparagus 8min\n2. Pan-sear salmon 6min skin\n3. Flip 2min\n4. Lemon + dill"},
            {"title": "Steak Green Beans", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 15, "calories": 480, "protein_g": 42, "carbs_g": 18, "fats_g": 26, "ingredients": "180g Steak\n200g Green beans\n1 tbsp Butter\nGarlic\nThyme", "instructions": "1. Steam beans\n2. Pan-sear steak 3min/side\n3. Sauté beans in butter\n4. Garlic + thyme"},
            
            # SNACK (1 recipe)
            {"title": "Date Almond Energy Balls", "category": "snack", "difficulty": "easy", "prep_time_minutes": 15, "calories": 180, "protein_g": 6, "carbs_g": 22, "fats_g": 8, "ingredients": "100g Dates\n50g Almonds\n20g Cacao\n1 tbsp Honey", "instructions": "1. Blend all ingredients\n2. Form balls\n3. Roll in cacao\n4. Refrigerate 30min"},
            
            # SHAKE (1 recipe)
            {"title": "Post-Workout Recovery Shake", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 350, "protein_g": 35, "carbs_g": 40, "fats_g": 5, "ingredients": "1 scoop Chocolate Whey\n1 Frozen banana\n200ml Water\n5g Creatine", "instructions": "1. All ingredients blender\n2. Blend smooth\n3. Drink immediately\n4. Post-workout"},
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
