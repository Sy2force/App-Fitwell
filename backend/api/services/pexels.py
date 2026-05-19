"""
Service Pexels pour récupérer des images optimisées
"""
import requests
from django.conf import settings
import os
from decouple import config
import hashlib

PEXELS_API_KEY = config('PEXELS_API_KEY', default='')

def get_pexels_image(query, orientation='portrait', size='large', page=1):
    """
    Récupère une image depuis Pexels API
    
    Args:
        query (str): Terme de recherche (ex: "fitness", "yoga", "nutrition")
        orientation (str): 'portrait', 'landscape', ou 'square'
        size (str): 'large', 'medium', ou 'small'
        page (int): Page de résultats pour éviter les doublons
    
    Returns:
        str: URL de l'image ou None si erreur
    """
    if not PEXELS_API_KEY:
        # Fallback vers Unsplash si pas de clé API
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
                # Récupérer l'image optimisée
                photo = data['photos'][0]
                
                # Choisir la taille appropriée
                if size == 'large':
                    return photo['src']['large']
                elif size == 'medium':
                    return photo['src']['medium']
                else:
                    return photo['src']['small']
        
        # Fallback si pas de résultat
        return get_unsplash_fallback(query, orientation)
        
    except Exception as e:
        print(f"Erreur Pexels API: {e}")
        return get_unsplash_fallback(query, orientation)


def get_unsplash_fallback(query, orientation='portrait'):
    """
    Fallback vers Unsplash si Pexels échoue
    
    Args:
        query (str): Terme de recherche
        orientation (str): 'portrait' ou 'landscape'
    
    Returns:
        str: URL Unsplash optimisée
    """
    # Dimensions optimisées
    if orientation == 'portrait':
        width, height = 800, 1000
    elif orientation == 'landscape':
        width, height = 1200, 800
    else:  # square
        width, height = 1000, 1000
    
    # Utiliser un hash plus grand pour éviter les collisions
    sig = abs(hash(query + orientation)) % 1000000
    
    # Paramètres d'optimisation Unsplash avec signature unique
    return f"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w={width}&h={height}&q=80&auto=format&fit=crop&sig={sig}"


def get_exercise_image(muscle_group, difficulty, title=None):
    """
    Récupère une image d'exercice optimisée
    
    Args:
        muscle_group (str): Groupe musculaire
        difficulty (str): Difficulté
        title (str): Titre de l'exercice (optionnel)
    
    Returns:
        str: URL de l'image
    """
    if title:
        # Utiliser le titre pour une recherche plus spécifique
        query = f"{title} {muscle_group} exercise fitness {difficulty}"
    else:
        query = f"{muscle_group} exercise fitness {difficulty}"
    
    # Utiliser le hash de la query pour déterminer la page de manière déterministe
    page = (hash(query) % 30) + 1
    return get_pexels_image(query, orientation='portrait', size='large', page=page)


def get_product_image(category, name=None):
    """
    Récupère une image de produit optimisée
    
    Args:
        category (str): Catégorie du produit
        name (str): Nom du produit (optionnel)
    
    Returns:
        str: URL de l'image
    """
    if name:
        # Utiliser le nom pour une recherche plus spécifique
        query = f"{name} {category} fitness equipment"
    else:
        query = f"{category} fitness equipment"
    
    # Utiliser le hash de la query pour déterminer la page de manière déterministe
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='square', size='large', page=page)


def get_recipe_image(category, title=None):
    """
    Récupère une image de recette optimisée
    
    Args:
        category (str): Catégorie de la recette
        title (str): Titre de la recette (optionnel)
    
    Returns:
        str: URL de l'image
    """
    if title:
        # Utiliser le titre pour une recherche plus spécifique
        query = f"{title} {category} healthy food"
    else:
        query = f"{category} healthy food"
    
    # Utiliser le hash de la query pour déterminer la page de manière déterministe
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='landscape', size='large', page=page)


def get_article_image(category, title=None):
    """
    Récupère une image d'article optimisée
    
    Args:
        category (str): Catégorie de l'article
        title (str): Titre de l'article (optionnel)
    
    Returns:
        str: URL de l'image
    """
    if title:
        # Utiliser le titre pour une recherche plus spécifique
        query = f"{title} {category} fitness lifestyle"
    else:
        query = f"{category} fitness lifestyle"
    
    # Utiliser le hash de la query pour déterminer la page de manière déterministe
    page = (hash(query) % 20) + 1
    return get_pexels_image(query, orientation='landscape', size='large', page=page)
