"""
Pexels service for retrieving optimized images
"""
import requests
from django.conf import settings
import os
from decouple import config
import hashlib

PEXELS_API_KEY = config('PEXELS_API_KEY', default='')

def get_pexels_image(query, orientation='portrait', size='large', page=1):
    """
    Retrieves an image from Pexels API
    
    Args:
        query (str): Search term (e.g., "fitness", "yoga", "nutrition")
        orientation (str): 'portrait', 'landscape', or 'square'
        size (str): 'large', 'medium', or 'small'
        page (int): Results page to avoid duplicates
    
    Returns:
        str: Image URL or None if error
    """
    if not PEXELS_API_KEY:
        # Fallback to Unsplash if no API key
        return get_unsplash_fallback(query, orientation)
    
    try:
        url = f"https://api.pexels.com/v1/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            "query": query,
            "per_page": 1,
            "orientation": orientation,
            "size": size,
            "page": page
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                # Retrieve optimized image
                photo = data['photos'][0]
                
                # Choose appropriate size
                if size == 'large':
                    return photo['src']['large']
                elif size == 'medium':
                    return photo['src']['medium']
                else:
                    return photo['src']['small']
        
        # Fallback if no result
        return get_unsplash_fallback(query, orientation)
        
    except Exception as e:
        print(f"Pexels API error: {e}")
        return get_unsplash_fallback(query, orientation)


def get_unsplash_fallback(query, orientation='portrait'):
    """
    Fallback to Unsplash if Pexels fails
    
    Args:
        query (str): Search term
        orientation (str): 'portrait' or 'landscape'
    
    Returns:
        str: Optimized Unsplash URL
    """
    # Optimized dimensions
    if orientation == 'portrait':
        width, height = 800, 1000
    elif orientation == 'landscape':
        width, height = 1200, 800
    else:  # square
        width, height = 1000, 1000
    
    # List of different Unsplash photos to avoid duplicates
    unsplash_photos = [
        "1571019613454-1cb2f99b2d8b",
        "1517836407607-4fe7391c4b6c",
        "1583454190589-92478f8d3d2e",
        "1534438327276-14e5300c3a48",
        "1552674605-469456971-97c",
        "1518310383802-5406943e45c",
        "1597356994534-98029738948f",
        "1576678927379-1a9f19b5b7c8",
        "1534438327276-14e5300c3a48",
        "1552674605-469456971-97c",
        "1517836407607-4fe7391c4b6c",
        "1583454190589-92478f8d3d2e",
        "1518310383802-5406943e45c",
        "1597356994534-98029738948f",
        "1576678927379-1a9f19b5b7c8",
        "1534438327276-14e5300c3a48",
        "1552674605-469456971-97c",
        "1517836407607-4fe7391c4b6c",
        "1583454190589-92478f8d3d2e",
        "1518310383802-5406943e45c",
    ]
    
    # Use query hash to select a different photo
    photo_index = abs(hash(query + orientation)) % len(unsplash_photos)
    photo_id = unsplash_photos[photo_index]
    
    # Unsplash optimization parameters
    return f"https://images.unsplash.com/photo-{photo_id}?w={width}&h={height}&q=80&auto=format&fit=crop"


def get_exercise_image(muscle_group, difficulty, title=None):
    """
    Retrieves an optimized exercise image
    
    Args:
        muscle_group (str): Muscle group
        difficulty (str): Difficulty
        title (str): Exercise title (optional)
    
    Returns:
        str: Image URL
    """
    if title:
        # Use title for more specific search
        query = f"{title} {muscle_group} exercise fitness {difficulty}"
    else:
        query = f"{muscle_group} exercise fitness {difficulty}"
    
    # Use query hash to deterministically determine page
    page = (hash(query) % 30) + 1
    return get_pexels_image(query, orientation='portrait', size='large', page=page)


def get_product_image(category, name=None):
    """
    Retrieves an optimized product image
    
    Args:
        category (str): Product category
        name (str): Product name (optional)
    
    Returns:
        str: Image URL
    """
    if name:
        # Use name for more specific search
        query = f"{name} {category} fitness equipment"
    else:
        query = f"{category} fitness equipment"
    
    # Use query hash to deterministically determine page
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='square', size='large', page=page)


def get_recipe_image(category, title=None):
    """
    Retrieves an optimized recipe image
    
    Args:
        category (str): Recipe category
        title (str): Recipe title (optional)
    
    Returns:
        str: Image URL
    """
    if title:
        # Use title for more specific search
        query = f"{title} {category} healthy food"
    else:
        query = f"{category} healthy food"
    
    # Use query hash to deterministically determine page
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='landscape', size='large', page=page)


def get_article_image(category, title=None):
    """
    Retrieves an optimized article image
    
    Args:
        category (str): Article category
        title (str): Article title (optional)
    
    Returns:
        str: Image URL
    """
    if title:
        # Use title for more specific search
        query = f"{title} {category} fitness lifestyle"
    else:
        query = f"{category} fitness lifestyle"
    
    # Use query hash to deterministically determine page
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='landscape', size='large', page=page)
