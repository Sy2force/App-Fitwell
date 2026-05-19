from django.core.management.base import BaseCommand
from api.models import Product
from api.services.pexels import get_product_image


class Command(BaseCommand):
    help = 'Seed the database with sample shop products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding shop products with Pexels API...')
        
        products_data = [
            # Musculation
            {
                'name': 'Haltères Ajustables 20kg',
                'slug': 'haltieres-ajustables-20kg',
                'category': 'strength',
                'brand': 'FitnessPro',
                'description_short': 'Set d\'haltères ajustables de 2 à 20kg pour tous les niveaux',
                'description_long': 'Set complet d\'haltères ajustables permettant de varier la charge de 2kg à 20kg par incréments de 2kg. Idéal pour l\'entraînement à domicile. Poignée ergonomique pour un confort optimal.',
                'price': 79.99,
                'old_price': 99.99,
                'rating': 4.5,
                'stock': 15,
                'features': ['Poids ajustable 2-20kg', 'Poignée ergonomique', 'Revêtement antidérapant', 'Idéal domicile'],
                'recommended_for': 'Débutants et intermédiaires pour l\'entraînement à domicile',
            },
            {
                'name': 'Barre de Musculation 150cm',
                'slug': 'barre-musculation-150cm',
                'category': 'strength',
                'brand': 'IronGym',
                'description_short': 'Barre olympique 150cm pour haltères et disques',
                'description_long': 'Barre olympique en acier de haute qualité, compatible avec tous les disques standards 50mm. Capacité de charge jusqu\'à 200kg.',
                'price': 59.99,
                'rating': 4.8,
                'stock': 20,
                'features': ['Acier trempé', 'Compatibilité olympique', 'Charge max 200kg', 'Grip antidérapant'],
                'recommended_for': 'Sportifs avancés pour musculation lourde',
            },
            # Cardio
            {
                'name': 'Vélo Élliptique Compact',
                'slug': 'velo-elliptique-compact',
                'category': 'cardio',
                'brand': 'CardioMaster',
                'description_short': 'Vélo elliptique pliable pour entraînement cardio à domicile',
                'description_long': 'Vélo elliptique compact avec résistance magnétique réglable à 8 niveaux. Écran LCD affichant temps, distance, calories et rythme cardiaque.',
                'price': 299.99,
                'old_price': 399.99,
                'rating': 4.3,
                'stock': 8,
                'features': ['8 niveaux de résistance', 'Écran LCD', 'Pliable', 'Silencieux'],
                'recommended_for': 'Cardio à domicile sans impact sur les articulations',
            },
            # Yoga & Mobilité
            {
                'name': 'Tapis de Yoga Premium',
                'slug': 'tapis-yoga-premium',
                'category': 'yoga',
                'brand': 'ZenMat',
                'description_short': 'Tapis de yoga 6mm antidérapant avec motif alignement',
                'description_long': 'Tapis de yoga de 6mm d\'épaisseur pour un confort optimal. Surface antidérapante avec lignes d\'alignement pour améliorer votre pratique.',
                'price': 39.99,
                'old_price': 49.99,
                'rating': 4.8,
                'stock': 25,
                'features': ['Épaisseur 6mm', 'Antidérapant', 'Lignes d\'alignement', 'Éco-responsable'],
                'recommended_for': 'Yoga, pilates, étirements et mobilité',
            },
            {
                'name': 'Tapis de Sport Évolutif',
                'slug': 'tapis-sport-evolutif',
                'category': 'yoga',
                'brand': 'FitFloor',
                'description_short': 'Tapis de sport polyvalent pour fitness et exercices au sol',
                'description_long': 'Tapis de sport haute densité avec amortissement supérieur. Surface texturée pour une meilleure adhérence. Idéal pour tous types d\'exercices au sol.',
                'price': 29.99,
                'rating': 4.6,
                'stock': 30,
                'features': ['Haute densité', 'Amortissement optimal', 'Surface texturée', 'Facile à nettoyer'],
                'recommended_for': 'Fitness, abdos, étirements et exercices au sol',
            },
            # Accessoires
            {
                'name': 'Barre de Traction Murale',
                'slug': 'barre-traction-murale',
                'category': 'accessories',
                'brand': 'PullUpPro',
                'description_short': 'Barre de traction murale en acier robuste',
                'description_long': 'Barre de traction murale en acier trempé, supporte jusqu\'à 150kg. Multiples prises pour varier les exercices. Installation facile avec kit inclus.',
                'price': 49.99,
                'rating': 4.7,
                'stock': 12,
                'features': ['Acier trempé', 'Charge max 150kg', 'Multiples prises', 'Kit installation inclus'],
                'recommended_for': 'Tractions, gainage et exercices dorsaux à domicile',
            },
            {
                'name': 'Kit Élastiques de Résistance',
                'slug': 'kit-elastiques-resistance',
                'category': 'accessories',
                'brand': 'FlexBand',
                'description_short': 'Set de 5 élastiques de résistance pour tous niveaux',
                'description_long': 'Kit complet de 5 élastiques avec résistances différentes (légère à extra-forte). Livrés avec sac de transport et guide d\'exercices. Idéal pour rééducation et renforcement.',
                'price': 24.99,
                'rating': 4.5,
                'stock': 40,
                'features': ['5 résistances', 'Sac transport inclus', 'Guide exercices', 'Durable'],
                'recommended_for': 'Renforcement musculaire, rééducation et entraînement à domicile',
            },
            # Nutrition
            {
                'name': 'Whey Protein Isolate 1kg',
                'slug': 'whey-protein-isolate-1kg',
                'category': 'nutrition',
                'brand': 'NutriMax',
                'description_short': 'Protéine whey isolate 90% pure pour récupération musculaire',
                'description_long': 'Whey protein isolate ultra-pure à 90% de protéines. Digestion rapide et absorption optimale. Riche en BCAA pour la récupération. Arôme chocolat naturel.',
                'price': 49.99,
                'rating': 4.7,
                'stock': 40,
                'features': ['90% protéines', 'Digestion rapide', 'Riche en BCAA', 'Sans sucre ajouté'],
                'recommended_for': 'Récupération musculaire après entraînement',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        # Use local SVG logo designs for all products
        product_logos = {
            'haltieres-ajustables-20kg': '/static/products/fitnesspro.svg',
            'barre-musculation-150cm': '/static/products/irongym.svg',
            'velo-elliptique-compact': '/static/products/cardiomaster.svg',
            'tapis-yoga-premium': '/static/products/zenmat.svg',
            'tapis-sport-evolutif': '/static/products/fitfloor.svg',
            'barre-traction-murale': '/static/products/pulluppro.svg',
            'kit-elastiques-resistance': '/static/products/flexband.svg',
            'whey-protein-isolate-1kg': '/static/products/nutrimax.svg',
        }
        
        for product_data in products_data:
            # Use local logo design
            image_url = product_logos.get(product_data['slug'], get_product_image(product_data['category'], product_data['name']))
            product_data['image'] = image_url
            
            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"Updated product: {product.name}")
        
        self.stdout.write(self.style.SUCCESS(f'\nShop products seeded successfully with Pexels! Created: {created_count}, Updated: {updated_count}'))
