from django.core.management.base import BaseCommand
from api.models import Product
from api.services.pexels import get_product_image


class Command(BaseCommand):
    help = 'Seed the database with sample shop products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding shop products with Pexels API...')
        
        products_data = [
            # Strength
            {
                'name': 'Adjustable Dumbbells 20kg',
                'slug': 'adjustable-dumbbells-20kg',
                'category': 'strength',
                'brand': 'FitnessPro',
                'description_short': 'Set of adjustable dumbbells from 2 to 20kg for all levels',
                'description_long': 'Complete set of adjustable dumbbells allowing you to vary the load from 2kg to 20kg in 2kg increments. Ideal for home training. Ergonomic grip for optimal comfort.',
                'price': 79.99,
                'old_price': 99.99,
                'rating': 4.5,
                'stock': 15,
                'features': ['Adjustable weight 2-20kg', 'Ergonomic grip', 'Non-slip coating', 'Ideal for home'],
                'recommended_for': 'Beginners and intermediates for home training',
            },
            {
                'name': 'Weightlifting Bar 150cm',
                'slug': 'weightlifting-bar-150cm',
                'category': 'strength',
                'brand': 'IronGym',
                'description_short': 'Olympic bar 150cm for dumbbells and plates',
                'description_long': 'High-quality steel Olympic bar, compatible with all standard 50mm plates. Load capacity up to 200kg.',
                'price': 59.99,
                'rating': 4.8,
                'stock': 20,
                'features': ['Tempered steel', 'Olympic compatibility', 'Max load 200kg', 'Non-slip grip'],
                'recommended_for': 'Advanced athletes for heavy weightlifting',
            },
            # Cardio
            {
                'name': 'Compact Elliptical Bike',
                'slug': 'compact-elliptical-bike',
                'category': 'cardio',
                'brand': 'CardioMaster',
                'description_short': 'Folding elliptical bike for home cardio training',
                'description_long': 'Compact elliptical bike with adjustable magnetic resistance at 8 levels. LCD screen displaying time, distance, calories and heart rate.',
                'price': 299.99,
                'old_price': 399.99,
                'rating': 4.3,
                'stock': 8,
                'features': ['8 resistance levels', 'LCD screen', 'Foldable', 'Quiet'],
                'recommended_for': 'Home cardio without joint impact',
            },
            # Yoga & Mobility
            {
                'name': 'Premium Yoga Mat',
                'slug': 'premium-yoga-mat',
                'category': 'yoga',
                'brand': 'ZenMat',
                'description_short': '6mm non-slip yoga mat with alignment pattern',
                'description_long': '6mm thick yoga mat for optimal comfort. Non-slip surface with alignment lines to improve your practice.',
                'price': 39.99,
                'old_price': 49.99,
                'rating': 4.8,
                'stock': 25,
                'features': ['6mm thickness', 'Non-slip', 'Alignment lines', 'Eco-friendly'],
                'recommended_for': 'Yoga, pilates, stretching and mobility',
            },
            {
                'name': 'Versatile Sports Mat',
                'slug': 'versatile-sports-mat',
                'category': 'yoga',
                'brand': 'FitFloor',
                'description_short': 'Versatile sports mat for fitness and floor exercises',
                'description_long': 'High-density sports mat with superior cushioning. Textured surface for better grip. Ideal for all types of floor exercises.',
                'price': 29.99,
                'rating': 4.6,
                'stock': 30,
                'features': ['High density', 'Optimal cushioning', 'Textured surface', 'Easy to clean'],
                'recommended_for': 'Fitness, abs, stretching and floor exercises',
            },
            # Accessories
            {
                'name': 'Wall Pull-Up Bar',
                'slug': 'wall-pull-up-bar',
                'category': 'accessories',
                'brand': 'PullUpPro',
                'description_short': 'Robust steel wall pull-up bar',
                'description_long': 'Tempered steel wall pull-up bar, supports up to 150kg. Multiple grips to vary exercises. Easy installation with included kit.',
                'price': 49.99,
                'rating': 4.7,
                'stock': 12,
                'features': ['Tempered steel', 'Max load 150kg', 'Multiple grips', 'Installation kit included'],
                'recommended_for': 'Pull-ups, core and back exercises at home',
            },
            {
                'name': 'Resistance Band Kit',
                'slug': 'resistance-band-kit',
                'category': 'accessories',
                'brand': 'FlexBand',
                'description_short': 'Set of 5 resistance bands for all levels',
                'description_long': 'Complete kit of 5 bands with different resistances (light to extra-heavy). Includes carrying bag and exercise guide. Ideal for rehabilitation and strengthening.',
                'price': 24.99,
                'rating': 4.5,
                'stock': 40,
                'features': ['5 resistances', 'Carrying bag included', 'Exercise guide', 'Durable'],
                'recommended_for': 'Muscle strengthening, rehabilitation and home training',
            },
            # Nutrition
            {
                'name': 'Whey Protein Isolate 1kg',
                'slug': 'whey-protein-isolate-1kg',
                'category': 'nutrition',
                'brand': 'NutriMax',
                'description_short': '90% pure whey protein isolate for muscle recovery',
                'description_long': 'Ultra-pure whey protein isolate with 90% protein content. Fast digestion and optimal absorption. Rich in BCAA for recovery. Natural chocolate flavor.',
                'price': 49.99,
                'rating': 4.7,
                'stock': 40,
                'features': ['90% protein', 'Fast digestion', 'BCAA rich', 'No added sugar'],
                'recommended_for': 'Muscle recovery after training',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        # Use local SVG logo designs for all products
        product_logos = {
            'adjustable-dumbbells-20kg': '/static/products/fitnesspro.svg',
            'weightlifting-bar-150cm': '/static/products/irongym.svg',
            'compact-elliptical-bike': '/static/products/cardiomaster.svg',
            'premium-yoga-mat': '/static/products/zenmat.svg',
            'versatile-sports-mat': '/static/products/fitfloor.svg',
            'wall-pull-up-bar': '/static/products/pulluppro.svg',
            'resistance-band-kit': '/static/products/flexband.svg',
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
