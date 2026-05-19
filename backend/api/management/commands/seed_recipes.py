from django.core.management.base import BaseCommand
from api.models import Recipe
from api.services.pexels import get_recipe_image

class Command(BaseCommand):
    help = 'Seeds 50+ complete recipes'

    def handle(self, *args, **kwargs):
        recipes = [
            # BREAKFAST (10 recettes)
            {"title": "Bowl Flocons d'Avoine Protéiné", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 10, "calories": 450, "protein_g": 30, "carbs_g": 55, "fats_g": 12, "ingredients": "80g Flocons d'avoine\n1 scoop Whey Vanille\n1 Banane\n10g Beurre cacahuète\n200ml Lait amande", "instructions": "1. Chauffer lait\n2. Mélanger flocons 2min\n3. Ajouter whey\n4. Garnir banane + beurre"},
            {"title": "Omelette Protéinée Épinards", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 12, "calories": 380, "protein_g": 35, "carbs_g": 8, "fats_g": 22, "ingredients": "4 Œufs\n50g Épinards frais\n30g Fromage feta\n1 c.s. Huile olive", "instructions": "1. Battre œufs\n2. Faire revenir épinards\n3. Verser œufs\n4. Ajouter feta, plier"},
            {"title": "Pancakes Protéinés Myrtilles", "category": "breakfast", "difficulty": "medium", "prep_time_minutes": 20, "calories": 420, "protein_g": 28, "carbs_g": 48, "fats_g": 10, "ingredients": "2 Œufs\n1 scoop Whey\n50g Flocons avoine\n100g Myrtilles\n1 c.c. Levure", "instructions": "1. Mixer œufs, whey, flocons\n2. Ajouter levure\n3. Cuire petites crêpes\n4. Garnir myrtilles"},
            {"title": "Avocado Toast Œufs Mollets", "category": "breakfast", "difficulty": "medium", "prep_time_minutes": 15, "calories": 480, "protein_g": 20, "carbs_g": 35, "fats_g": 28, "ingredients": "2 Pain complet\n1/2 Avocat\n2 Œufs\nPiment Espelette", "instructions": "1. Griller pain\n2. Écraser avocat\n3. Œufs 6min eau bouillante\n4. Assembler, pimenter"},
            {"title": "Yaourt Grec Granola Fruits", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 5, "calories": 380, "protein_g": 25, "carbs_g": 45, "fats_g": 12, "ingredients": "200g Yaourt grec 0%\n40g Granola\n100g Fruits rouges\n10g Miel", "instructions": "1. Verser yaourt\n2. Ajouter granola\n3. Garnir fruits\n4. Filet miel"},
            {"title": "Smoothie Bowl Açaï", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 10, "calories": 410, "protein_g": 22, "carbs_g": 52, "fats_g": 14, "ingredients": "1 sachet Açaï surgelé\n1 Banane\n1 scoop Whey\n30g Granola\n10g Coco râpée", "instructions": "1. Mixer açaï + banane + whey\n2. Verser bol\n3. Garnir granola\n4. Parsemer coco"},
            {"title": "Œufs Brouillés Saumon Fumé", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 10, "calories": 420, "protein_g": 32, "carbs_g": 12, "fats_g": 28, "ingredients": "3 Œufs\n50g Saumon fumé\n1 Pain complet\n10g Beurre\nAneth", "instructions": "1. Battre œufs\n2. Cuire doucement au beurre\n3. Ajouter saumon émietté\n4. Servir sur pain grillé"},
            {"title": "Porridge Banane Cannelle", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 12, "calories": 390, "protein_g": 18, "carbs_g": 58, "fats_g": 10, "ingredients": "60g Flocons avoine\n250ml Lait\n1 Banane\nCannelle\n15g Noix", "instructions": "1. Cuire flocons dans lait 5min\n2. Écraser 1/2 banane dedans\n3. Garnir reste banane\n4. Cannelle + noix"},
            {"title": "Toast Beurre Cacahuète Banane", "category": "breakfast", "difficulty": "easy", "prep_time_minutes": 5, "calories": 400, "protein_g": 16, "carbs_g": 48, "fats_g": 18, "ingredients": "2 Pain complet\n25g Beurre cacahuète\n1 Banane\nCannelle", "instructions": "1. Griller pain\n2. Tartiner beurre cacahuète\n3. Trancher banane dessus\n4. Saupoudrer cannelle"},
            {"title": "Crêpes Protéinées Chocolat", "category": "breakfast", "difficulty": "medium", "prep_time_minutes": 18, "calories": 440, "protein_g": 30, "carbs_g": 42, "fats_g": 14, "ingredients": "3 Œufs\n1 scoop Whey chocolat\n40g Farine avoine\n150ml Lait\n1 c.c. Cacao", "instructions": "1. Mixer tous ingrédients\n2. Laisser reposer 5min\n3. Cuire crêpes fines\n4. Empiler"},
            
            # LUNCH (10 recettes)
            {"title": "Poulet Rôti Patates Douces", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 35, "calories": 600, "protein_g": 45, "carbs_g": 60, "fats_g": 15, "ingredients": "150g Poulet\n200g Patate douce\n100g Brocolis\n1 c.s. Huile olive\nPaprika", "instructions": "1. Four 200°C\n2. Couper patates + poulet\n3. Huile + épices\n4. Cuire 25-30min"},
            {"title": "Bowl Buddha Quinoa Poulet", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 30, "calories": 580, "protein_g": 42, "carbs_g": 55, "fats_g": 18, "ingredients": "150g Poulet\n80g Quinoa\n100g Pois chiches\n50g Avocat\nTahini", "instructions": "1. Cuire quinoa\n2. Rôtir poulet + pois chiches\n3. Assembler bowl\n4. Sauce tahini"},
            {"title": "Wrap Thon Avocat", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 10, "calories": 520, "protein_g": 38, "carbs_g": 42, "fats_g": 20, "ingredients": "1 Tortilla complète\n150g Thon conserve\n1/2 Avocat\nLaitue\nTomate", "instructions": "1. Égoutter thon\n2. Écraser avocat\n3. Garnir tortilla\n4. Rouler serré"},
            {"title": "Riz Poulet Teriyaki", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 25, "calories": 620, "protein_g": 48, "carbs_g": 68, "fats_g": 14, "ingredients": "150g Poulet\n100g Riz basmati\nSauce teriyaki\nBrocolis\nSésame", "instructions": "1. Cuire riz\n2. Poêler poulet\n3. Ajouter sauce teriyaki\n4. Servir avec brocolis vapeur"},
            {"title": "Salade César Poulet Grillé", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 15, "calories": 480, "protein_g": 40, "carbs_g": 22, "fats_g": 26, "ingredients": "150g Poulet\nRomaine\n30g Parmesan\nCroûtons\nSauce césar", "instructions": "1. Griller poulet\n2. Laver romaine\n3. Assembler salade\n4. Sauce + parmesan"},
            {"title": "Pâtes Bolognaise Protéinée", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 30, "calories": 640, "protein_g": 52, "carbs_g": 72, "fats_g": 16, "ingredients": "100g Pâtes complètes\n150g Bœuf haché 5%\nSauce tomate\nOignon\nAil", "instructions": "1. Cuire pâtes\n2. Faire revenir viande\n3. Ajouter sauce tomate\n4. Mélanger pâtes"},
            {"title": "Burger Maison Fitness", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 20, "calories": 580, "protein_g": 45, "carbs_g": 48, "fats_g": 20, "ingredients": "150g Steak haché 5%\n1 Pain burger complet\nLaitue\nTomate\nOignon", "instructions": "1. Former steak\n2. Griller 4min/côté\n3. Toaster pain\n4. Assembler burger"},
            {"title": "Wok Crevettes Légumes", "category": "lunch", "difficulty": "medium", "prep_time_minutes": 18, "calories": 420, "protein_g": 38, "carbs_g": 45, "fats_g": 10, "ingredients": "200g Crevettes\n100g Riz\nPoivrons\nOignons\nSauce soja", "instructions": "1. Cuire riz\n2. Wok très chaud\n3. Sauter crevettes + légumes\n4. Sauce soja"},
            {"title": "Tacos Poulet Épicé", "category": "lunch", "difficulty": "easy", "prep_time_minutes": 20, "calories": 540, "protein_g": 42, "carbs_g": 52, "fats_g": 16, "ingredients": "150g Poulet\n3 Tortillas maïs\nHaricots noirs\nSalsa\nCoriandre", "instructions": "1. Épicer + cuire poulet\n2. Chauffer haricots\n3. Garnir tortillas\n4. Salsa + coriandre"},
            {"title": "Pizza Protéinée Maison", "category": "lunch", "difficulty": "hard", "prep_time_minutes": 45, "calories": 620, "protein_g": 48, "carbs_g": 65, "fats_g": 18, "ingredients": "Pâte pizza protéinée\nSauce tomate\n150g Poulet\nMozzarella light\nLégumes", "instructions": "1. Étaler pâte\n2. Sauce tomate\n3. Garnir poulet + légumes\n4. Four 220°C 15min"},
            
            # DINNER (8 recettes)
            {"title": "Saumon Grillé Asperges", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 20, "calories": 520, "protein_g": 35, "carbs_g": 10, "fats_g": 35, "ingredients": "150g Saumon\n200g Asperges\nCitron\nAneth\n15g Amandes", "instructions": "1. Asperges vapeur 8min\n2. Poêler saumon 6min peau\n3. Retourner 2min\n4. Citron + aneth"},
            {"title": "Steak Haricots Verts", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 15, "calories": 480, "protein_g": 42, "carbs_g": 18, "fats_g": 26, "ingredients": "180g Steak\n200g Haricots verts\n1 c.s. Beurre\nAil\nThym", "instructions": "1. Cuire haricots vapeur\n2. Poêler steak 3min/côté\n3. Faire revenir haricots au beurre\n4. Ail + thym"},
            {"title": "Poulet Curry Coco", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 30, "calories": 560, "protein_g": 44, "carbs_g": 38, "fats_g": 24, "ingredients": "150g Poulet\n100g Riz basmati\nLait coco light\nPâte curry\nÉpinards", "instructions": "1. Cuire riz\n2. Faire revenir poulet\n3. Ajouter curry + lait coco\n4. Épinards dernière minute"},
            {"title": "Thon Mi-Cuit Salade", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 12, "calories": 420, "protein_g": 38, "carbs_g": 12, "fats_g": 24, "ingredients": "150g Thon frais\nMesclun\nTomates cerises\nHuile sésame\nSésame", "instructions": "1. Saisir thon 1min/côté\n2. Laisser rosé au centre\n3. Trancher finement\n4. Servir sur salade"},
            {"title": "Crevettes Ail Courgettes", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 15, "calories": 380, "protein_g": 36, "carbs_g": 22, "fats_g": 16, "ingredients": "200g Crevettes\n2 Courgettes\n3 Gousses ail\nHuile olive\nPersil", "instructions": "1. Tailler courgettes spaghetti\n2. Faire revenir ail\n3. Ajouter crevettes 3min\n4. Mélanger courgettes"},
            {"title": "Omelette Légumes Fromage", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 12, "calories": 420, "protein_g": 32, "carbs_g": 14, "fats_g": 26, "ingredients": "4 Œufs\nPoivrons\nChampignons\n40g Fromage râpé\nHerbes", "instructions": "1. Faire revenir légumes\n2. Battre œufs\n3. Verser sur légumes\n4. Fromage + plier"},
            {"title": "Cabillaud Ratatouille", "category": "dinner", "difficulty": "medium", "prep_time_minutes": 35, "calories": 440, "protein_g": 38, "carbs_g": 28, "fats_g": 18, "ingredients": "150g Cabillaud\nAubergine\nCourgette\nPoivron\nTomates", "instructions": "1. Préparer ratatouille\n2. Cuire légumes 20min\n3. Poêler cabillaud 4min/côté\n4. Servir ensemble"},
            {"title": "Bœuf Sauté Brocolis", "category": "dinner", "difficulty": "easy", "prep_time_minutes": 18, "calories": 520, "protein_g": 44, "carbs_g": 20, "fats_g": 28, "ingredients": "150g Bœuf émincé\n200g Brocolis\nSauce soja\nGingembre\nAil", "instructions": "1. Wok très chaud\n2. Saisir bœuf 2min\n3. Ajouter brocolis\n4. Sauce soja + gingembre"},
            
            # SNACK (6 recettes)
            {"title": "Energy Balls Dattes Amandes", "category": "snack", "difficulty": "easy", "prep_time_minutes": 15, "calories": 180, "protein_g": 6, "carbs_g": 22, "fats_g": 8, "ingredients": "100g Dattes\n50g Amandes\n20g Cacao\n1 c.s. Miel", "instructions": "1. Mixer tous ingrédients\n2. Former boules\n3. Rouler dans cacao\n4. Réfrigérer 30min"},
            {"title": "Cottage Cheese Fruits", "category": "snack", "difficulty": "easy", "prep_time_minutes": 5, "calories": 220, "protein_g": 20, "carbs_g": 24, "fats_g": 4, "ingredients": "150g Cottage cheese\n100g Fruits rouges\n10g Miel\nCannelle", "instructions": "1. Verser cottage\n2. Ajouter fruits\n3. Miel + cannelle\n4. Mélanger"},
            {"title": "Barre Protéinée Maison", "category": "snack", "difficulty": "medium", "prep_time_minutes": 30, "calories": 240, "protein_g": 18, "carbs_g": 26, "fats_g": 8, "ingredients": "2 scoops Whey\n80g Flocons avoine\n30g Beurre cacahuète\n50ml Lait", "instructions": "1. Mélanger tous ingrédients\n2. Presser dans moule\n3. Réfrigérer 2h\n4. Couper barres"},
            {"title": "Pomme Beurre Amande", "category": "snack", "difficulty": "easy", "prep_time_minutes": 3, "calories": 200, "protein_g": 6, "carbs_g": 28, "fats_g": 8, "ingredients": "1 Pomme\n20g Beurre amande\nCannelle", "instructions": "1. Trancher pomme\n2. Tartiner beurre amande\n3. Saupoudrer cannelle\n4. Déguster"},
            {"title": "Houmous Légumes Croquants", "category": "snack", "difficulty": "easy", "prep_time_minutes": 10, "calories": 180, "protein_g": 8, "carbs_g": 20, "fats_g": 8, "ingredients": "100g Houmous\nCarottes\nCéleri\nPoivron\nConcombre", "instructions": "1. Couper légumes bâtonnets\n2. Disposer houmous\n3. Tremper légumes\n4. Déguster"},
            
            # SHAKE (5 recettes)
            {"title": "Shake Post-Workout Récup", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 350, "protein_g": 35, "carbs_g": 40, "fats_g": 5, "ingredients": "1 scoop Whey Chocolat\n1 Banane surgelée\n200ml Eau\n5g Créatine", "instructions": "1. Tous ingrédients blender\n2. Mixer lisse\n3. Boire immédiatement\n4. Post-workout"},
            {"title": "Smoothie Vert Détox", "category": "shake", "difficulty": "easy", "prep_time_minutes": 8, "calories": 280, "protein_g": 22, "carbs_g": 35, "fats_g": 6, "ingredients": "1 scoop Whey Vanille\nÉpinards\n1 Pomme verte\nConcombre\nGingembre", "instructions": "1. Laver légumes\n2. Mixer tous ingrédients\n3. Ajouter eau si besoin\n4. Boire frais"},
            {"title": "Shake Masse Gaineur", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 580, "protein_g": 42, "carbs_g": 68, "fats_g": 14, "ingredients": "2 scoops Whey\n80g Flocons avoine\n1 Banane\n30g Beurre cacahuète\n300ml Lait", "instructions": "1. Mixer tous ingrédients\n2. Texture épaisse\n3. Boire lentement\n4. Entre repas"},
            {"title": "Smoothie Fruits Rouges", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 320, "protein_g": 28, "carbs_g": 38, "fats_g": 6, "ingredients": "1 scoop Whey Fraise\n150g Fruits rouges surgelés\n100g Yaourt grec\n150ml Eau", "instructions": "1. Mixer tous ingrédients\n2. Texture smoothie\n3. Boire frais\n4. Collation"},
            {"title": "Shake Café Protéiné", "category": "shake", "difficulty": "easy", "prep_time_minutes": 5, "calories": 280, "protein_g": 30, "carbs_g": 24, "fats_g": 8, "ingredients": "1 scoop Whey Vanille\n1 Espresso froid\n200ml Lait amande\nGlace\nCannelle", "instructions": "1. Préparer café froid\n2. Mixer avec whey + lait\n3. Ajouter glace\n4. Cannelle dessus"},
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
