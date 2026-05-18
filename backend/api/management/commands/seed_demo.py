from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all seed commands to populate the database with demo data'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Starting complete demo data seeding...\n')
        
        commands = [
            ('seed_db', 'Admin + Categories'),
            ('seed_exercises', '101 Exercises'),
            ('seed_blog', '5 Blog Articles'),
            ('seed_badges', '20 Badges'),
            ('seed_recipes', '39 Recipes'),
            ('seed_programs', '3 Training Programs'),
            ('seed_shop', '13 Shop Products'),
            ('seed_demo_user', 'Demo User'),
        ]
        
        for command_name, description in commands:
            self.stdout.write(f'\n🔄 {description}...')
            try:
                call_command(command_name)
                self.stdout.write(self.style.SUCCESS(f'✅ {description} completed'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ {description} failed: {str(e)}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 Demo data seeding complete!'))
        self.stdout.write('='*50)
        self.stdout.write('\n📝 Demo Accounts:')
        self.stdout.write('  Admin: admin / adminpassword')
        self.stdout.write('  Demo: demo@fitwell.com / demo123')
        self.stdout.write('\n📊 Data Summary:')
        self.stdout.write('  - 101 Exercises')
        self.stdout.write('  - 39 Recipes')
        self.stdout.write('  - 5 Articles')
        self.stdout.write('  - 20 Badges')
        self.stdout.write('  - 3 Programs')
        self.stdout.write('  - 13 Products')
        self.stdout.write('  - 9 Users (including admin + demo)')
