from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from web.forms import CommentForm
from api.models import Article, Category, Comment, Exercise, Recipe

def exercise_library(request):
    """
    Exercise library.
    Allows filtering by muscle group, difficulty and text search.
    """
    exercises = Exercise.objects.all()
    
    # Search query
    search_query = request.GET.get('search')
    if search_query:
        exercises = exercises.filter(name__icontains=search_query)
    
    # Muscle group filter
    muscle = request.GET.get('muscle')
    if muscle:
        exercises = exercises.filter(muscle_group=muscle)
    
    # Difficulty filter
    difficulty = request.GET.get('difficulty')
    if difficulty:
        exercises = exercises.filter(difficulty=difficulty)
        
    return render(request, 'web/exercise_library.html', {
        'exercises': exercises,
        'current_muscle': muscle,
        'current_difficulty': difficulty,
        'muscle_choices': Exercise.MUSCLE_CHOICES,
        'search_query': search_query
    })

def exercise_detail(request, slug):
    """
    Exercise detail with full instructions.
    """
    exercise = get_object_or_404(Exercise, slug=slug)
    
    # Similar exercises (same muscle group)
    similar_exercises = Exercise.objects.filter(
        muscle_group=exercise.muscle_group
    ).exclude(id=exercise.id)[:4]
    
    context = {
        'exercise': exercise,
        'similar_exercises': similar_exercises,
    }
    return render(request, 'web/exercise_detail.html', context)

def recipe_list(request):
    """
    Nutrition recipe list.
    Filtering by category (breakfast, dinner...) and difficulty.
    """
    recipes = Recipe.objects.all()
    
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    if category:
        recipes = recipes.filter(category=category)
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
        
    return render(request, 'web/recipe_list.html', {
        'recipes': recipes,
        'current_category': category,
        'current_difficulty': difficulty,
        'category_choices': Recipe.CATEGORY_CHOICES
    })

def recipe_detail(request, recipe_id):
    """
    Recipe detail with macro percentage calculations.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Calculate Macro Percentages
    cal_protein = recipe.protein_g * 4
    cal_carbs = recipe.carbs_g * 4
    cal_fats = recipe.fats_g * 9
    
    total_cal_calc = cal_protein + cal_carbs + cal_fats
    
    context = {
        'recipe': recipe,
        'pct_protein': 0,
        'pct_carbs': 0,
        'pct_fats': 0
    }
    
    if total_cal_calc > 0:
        context['pct_protein'] = int((cal_protein / total_cal_calc) * 100)
        context['pct_carbs'] = int((cal_carbs / total_cal_calc) * 100)
        context['pct_fats'] = int((cal_fats / total_cal_calc) * 100)
        
    return render(request, 'web/recipe_detail.html', context)

def blog_list(request):
    """
    Blog article list.
    Supports text search and category filtering.
    """
    # Update Streak if reading blog
    if request.user.is_authenticated and hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    # Optimized: select_related for author and category
    articles = Article.objects.filter(is_published=True).select_related('author', 'category')
    categories = Category.objects.all()
    
    # Search
    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query) | articles.filter(content__icontains=query)
        
    # Filter by Category
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        
    articles = articles.order_by('-created_at').distinct()
    
    return render(request, 'web/blog_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': category_slug,
        'search_query': query
    })

def article_detail(request, slug):
    """
    Reading a full article.
    Allows liking and commenting.
    Shows similar articles at the bottom of the page.
    """
    # Update Streak if reading article
    if request.user.is_authenticated and hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    # Optimized: select_related for author and category, prefetch comments with authors
    article = get_object_or_404(
        Article.objects.select_related('author', 'category').prefetch_related('comments__author'),
        slug=slug,
        is_published=True
    )
    comments = article.comments.select_related('author').order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, _("Your opinion has been shared! ✨"))
            return redirect('article_detail', slug=slug)
    else:
        form = CommentForm()
        
    is_liked = False
    if request.user.is_authenticated:
        is_liked = article.likes.filter(id=request.user.id).exists()
        
    # Related Articles (optimized)
    related_articles = []
    if article.category:
        related_articles = Article.objects.filter(
            category=article.category, 
            is_published=True
        ).exclude(id=article.id).select_related('author', 'category').only(
            'title', 'slug', 'image', 'created_at', 'author__username', 'category__name'
        ).order_by('-created_at')[:3]
        
    return render(request, 'web/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'related_articles': related_articles
    })

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Ensure user is the author of the comment
    if request.user == comment.author:
        article_slug = comment.article.slug
        comment.delete()
        messages.success(request, _("Your comment has been removed."))
        return redirect('article_detail', slug=article_slug)
    else:
        messages.error(request, _("You are not authorized to remove this comment."))
        return redirect('article_detail', slug=comment.article.slug)

@login_required(login_url='login')
def like_article(request, slug):
    # Like action also counts for streak
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    article = get_object_or_404(Article, slug=slug)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article_detail', slug=slug)
