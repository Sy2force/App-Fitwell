from django.core.management.base import BaseCommand
from api.models import Exercise, Product, Recipe, Article
from collections import Counter

class Command(BaseCommand):
    help = 'Check images for completeness and duplicates'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🔍 Checking Images...'))
        
        # Collect all image URLs
        all_images = []
        
        # Exercises
        exercises = Exercise.objects.all()
        for ex in exercises:
            if ex.image_url:
                all_images.append(('exercise', ex.name, ex.image_url))
        
        # Products
        products = Product.objects.all()
        for prod in products:
            if prod.image:
                all_images.append(('product', prod.name, prod.image))
        
        # Recipes
        recipes = Recipe.objects.all()
        for rec in recipes:
            if rec.image_url:
                all_images.append(('recipe', rec.title, rec.image_url))
        
        # Articles
        articles = Article.objects.all()
        for art in articles:
            if art.image:
                all_images.append(('article', art.title, art.image))
        
        # Statistics
        total_items = len(all_images)
        unique_urls = len(set(img[2] for img in all_images))
        duplicates = total_items - unique_urls
        
        self.stdout.write(f'\n📊 Statistics:')
        self.stdout.write(f'   Total items with images: {total_items}')
        self.stdout.write(f'   Unique image URLs: {unique_urls}')
        self.stdout.write(f'   Duplicates: {duplicates}')
        
        # Check for missing images
        missing_exercises = Exercise.objects.filter(image_url__isnull=True).count()
        missing_products = Product.objects.filter(image__isnull=True).count()
        missing_recipes = Recipe.objects.filter(image_url__isnull=True).count()
        missing_articles = Article.objects.filter(image__isnull=True).count()
        
        self.stdout.write(f'\n❌ Missing images:')
        self.stdout.write(f'   Exercises: {missing_exercises}')
        self.stdout.write(f'   Products: {missing_products}')
        self.stdout.write(f'   Recipes: {missing_recipes}')
        self.stdout.write(f'   Articles: {missing_articles}')
        
        # Check duplicates
        if duplicates > 0:
            url_counter = Counter(img[2] for img in all_images)
            duplicate_urls = {url: count for url, count in url_counter.items() if count > 1}
            
            self.stdout.write(f'\n🔁 Duplicate URLs ({len(duplicate_urls)}):')
            for url, count in duplicate_urls.items():
                items = [img[1] for img in all_images if img[2] == url]
                self.stdout.write(f'   URL: {url[:80]}...')
                self.stdout.write(f'   Used {count} times by: {", ".join(items[:5])}')
        else:
            self.stdout.write(f'\n✅ No duplicates found!')
        
        # Check if at least 50 unique images
        if unique_urls >= 50:
            self.stdout.write(f'\n✅ {unique_urls} unique images (>= 50) - OK!')
        else:
            self.stdout.write(f'\n❌ Only {unique_urls} unique images (< 50) - Need more variety!')
