from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.models import User, Favorite, Cart, CartItem, Product, Exercise, Recipe, Program, UserProgramProgress


class Command(BaseCommand):
    help = 'Create a demo user with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo user...')
        
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            email='demo@fitwell.com',
            defaults={
                'username': 'demo',
                'password': make_password('demo123'),
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True,
                'is_verified': True,
                'is_onboarded': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created demo user: {demo_user.email}"))
        else:
            self.stdout.write(f"Demo user already exists: {demo_user.email}")
        
        # Create UserStats if not exists
        if not hasattr(demo_user, 'stats'):
            from api.models import UserStats
            UserStats.objects.create(
                user=demo_user,
                xp=500,
                level=2,
                streak_days=7,
                last_activity_date=None
            )
            self.stdout.write(self.style.SUCCESS("Created UserStats for demo user"))
        
        # Add sample favorites
        exercises = Exercise.objects.all()[:3]
        recipes = Recipe.objects.all()[:2]
        products = Product.objects.all()[:2]
        
        for exercise in exercises:
            Favorite.objects.get_or_create(
                user=demo_user,
                content_type='exercise',
                exercise=exercise,
                defaults={'notes': 'Excellent exercice pour le haut du corps'}
            )
        
        for recipe in recipes:
            Favorite.objects.get_or_create(
                user=demo_user,
                content_type='recipe',
                recipe=recipe,
                defaults={'notes': 'Délicieuse et facile à préparer'}
            )
        
        for product in products:
            Favorite.objects.get_or_create(
                user=demo_user,
                content_type='product',
                product=product,
                defaults={'notes': 'Ajouté à ma liste de souhaits'}
            )
        
        self.stdout.write(self.style.SUCCESS(f"Added {len(exercises) + len(recipes) + len(products)} favorites"))
        
        # Create cart with sample items
        cart, created = Cart.objects.get_or_create(
            user=demo_user
        )
        
        shop_products = Product.objects.all()[:2]
        for product in shop_products:
            CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 1}
            )
        
        self.stdout.write(self.style.SUCCESS(f"Created cart with {len(shop_products)} items"))
        
        # Add program progress
        programs = Program.objects.all()[:1]
        for program in programs:
            UserProgramProgress.objects.get_or_create(
                user=demo_user,
                program=program,
                defaults={
                    'current_day': 3,
                    'status': 'in_progress',
                    'started_at': None
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f"Added program progress for {len(programs)} program(s)"))
        
        self.stdout.write(self.style.SUCCESS('\nDemo user created successfully!'))
        self.stdout.write(self.style.WARNING('Email: demo@fitwell.com'))
        self.stdout.write(self.style.WARNING('Password: demo123'))
