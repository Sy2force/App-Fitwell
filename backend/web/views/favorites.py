from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models import Favorite, Exercise, Recipe, Product


@login_required
def favorites_view(request):
    """
    List of all user favorites (exercises, recipes, products).
    """
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'exercise', 'recipe', 'product'
    )
    
    # Filter by content type
    content_type_filter = request.GET.get('type')
    if content_type_filter:
        favorites = favorites.filter(content_type=content_type_filter)
    
    context = {
        'favorites': favorites,
        'content_type_filter': content_type_filter,
    }
    return render(request, 'web/favorites.html', context)


@login_required
def add_favorite(request, content_type, content_id):
    """
    Add content to favorites.
    content_type: 'exercise', 'recipe', 'product'
    """
    if content_type == 'exercise':
        content = get_object_or_404(Exercise, id=content_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type='exercise',
            exercise=content
        )
    elif content_type == 'recipe':
        content = get_object_or_404(Recipe, id=content_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type='recipe',
            recipe=content
        )
    elif content_type == 'product':
        content = get_object_or_404(Product, id=content_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type='product',
            product=content
        )
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    if created:
        # Award small XP for adding favorite
        if hasattr(request.user, 'stats'):
            request.user.stats.add_xp(5)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_favorite(request, favorite_id):
    """
    Remove a favorite.
    """
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
