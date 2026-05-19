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
            {
                'name': 'Kit Disques 50kg',
                'slug': 'kit-disques-50kg',
                'category': 'strength',
                'brand': 'PowerFit',
                'description_short': 'Kit complet de disques de 2 à 20kg',
                'description_long': 'Kit de disques incluant 2x20kg, 2x10kg, 2x5kg, 2x2.5kg et 2x1.25kg. Revêtement en caoutchouc pour protéger vos sols.',
                'price': 149.99,
                'old_price': 179.99,
                'rating': 4.6,
                'stock': 10,
                'features': ['Total 50kg', 'Revêtement caoutchouc', 'Disques standards 50mm', 'Support inclus'],
                'recommended_for': 'Programme de musculation complet à domicile',
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
            {
                'name': 'Corde à Sauter Pro',
                'slug': 'corde-a-sauter-pro',
                'category': 'cardio',
                'brand': 'SpeedRope',
                'description_short': 'Corde à sauter professionnelle avec compteurs',
                'description_long': 'Corde à sauter en acier avec revêtement PVC pour durabilité maximale. Compteur intégré pour suivre vos sauts. Poignées ergonomiques antidérapantes.',
                'price': 19.99,
                'rating': 4.7,
                'stock': 50,
                'features': ['Compteur intégré', 'Poignées ergonomiques', 'Câble acier', 'Réglable'],
                'recommended_for': 'Cardio rapide et efficace n\'importe où',
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
                'name': 'Rouleau de Massage',
                'slug': 'rouleau-massage',
                'category': 'yoga',
                'brand': 'RecoveryPro',
                'description_short': 'Rouleau de massage en mousse pour récupération musculaire',
                'description_long': 'Rouleau de massage haute densité pour libérer les tensions musculaires. Idéal après l\'entraînement pour accélérer la récupération.',
                'price': 24.99,
                'rating': 4.5,
                'stock': 30,
                'features': ['Mousse haute densité', 'Soulage les tensions', 'Léger et portable', 'Antidérapant'],
                'recommended_for': 'Récupération musculaire et mobilité',
            },
            # Vêtements
            {
                'name': 'T-shirt Performance Homme',
                'slug': 'tshirt-performance-homme',
                'category': 'clothing',
                'brand': 'FitWear',
                'description_short': 'T-shirt technique respirant pour l\'entraînement',
                'description_long': 'T-shirt en polyester respirant avec technologie d\'évaporation de l\'humidité. Coupe ajustée pour liberté de mouvement optimale.',
                'price': 29.99,
                'rating': 4.4,
                'stock': 100,
                'features': ['Polyester respirant', 'Technologie dry-fit', 'Coupe ajustée', 'Machine lavable'],
                'recommended_for': 'Entraînement intensif et compétition',
            },
            {
                'name': 'Legging Yoga Femme',
                'slug': 'legging-yoga-femme',
                'category': 'clothing',
                'brand': 'FitWear',
                'description_short': 'Legging haute taille pour yoga et fitness',
                'description_long': 'Legging en tissu extensible avec taille haute pour un maintien optimal. Poches latérales pratiques. Idéal pour yoga, pilates et fitness.',
                'price': 34.99,
                'old_price': 44.99,
                'rating': 4.6,
                'stock': 80,
                'features': ['Taille haute', 'Tissu extensible', 'Poches latérales', 'Absorbant'],
                'recommended_for': 'Yoga, pilates, fitness et loisirs',
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
            {
                'name': 'BCAA 2:1:1 500g',
                'slug': 'bcaa-211-500g',
                'category': 'nutrition',
                'brand': 'NutriMax',
                'description_short': 'Acides aminés branchés pour protection musculaire',
                'description_long': 'BCAA ratio 2:1:1 (leucine, isoleucine, valine) pour protéger et reconstruire le muscle. Arôme fruits rouges. Idéal pendant l\'entraînement.',
                'price': 24.99,
                'rating': 4.5,
                'stock': 35,
                'features': ['Ratio 2:1:1', 'Protection musculaire', 'Arôme naturel', 'Sans aspartame'],
                'recommended_for': 'Pendant l\'entraînement pour protéger le muscle',
            },
            # Accessoires
            {
                'name': 'Gourde Isotermique 750ml',
                'slug': 'gourde-isotermique-750ml',
                'category': 'accessories',
                'brand': 'HydroFit',
                'description_short': 'Gourde inox double paroi pour garder vos boissons au frais',
                'description_long': 'Gourde en inox 18/8 avec double paroi isotherme. Garde vos boissons froides jusqu\'à 24h ou chaudes jusqu\'à 12h. Bouchon étanche.',
                'price': 19.99,
                'rating': 4.6,
                'stock': 60,
                'features': ['Inox 18/8', 'Double paroi', 'Étanche', 'BPA-free'],
                'recommended_for': 'Hydratation pendant et après l\'entraînement',
            },
            {
                'name': 'Sac de Sport 40L',
                'slug': 'sac-de-sport-40l',
                'category': 'accessories',
                'brand': 'SportGear',
                'description_short': 'Sac de sport spacieux avec compartiment pour chaussures',
                'description_long': 'Sac de sport 40L avec compartiment ventilé pour chaussures. Multiples poches pour organisation. Bandoulière rembourrée pour confort.',
                'price': 44.99,
                'old_price': 59.99,
                'rating': 4.4,
                'stock': 25,
                'features': ['40L capacité', 'Compartiment chaussures', 'Multiples poches', 'Bandoulière confort'],
                'recommended_for': 'Transport de tout votre équipement sportif',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for product_data in products_data:
            # Fetch image from Pexels API with name for more specific search
            image_url = get_product_image(product_data['category'], product_data['name'])
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
