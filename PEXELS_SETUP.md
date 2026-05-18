# Configuration Pexels API pour Production (Render)

## Ajouter la clé API Pexels sur Render

1. Allez sur le dashboard Render : https://dashboard.render.com/
2. Sélectionnez le service "fitwell"
3. Cliquez sur "Environment" dans le menu de gauche
4. Cliquez sur "Add Environment Variable"
5. Ajoutez :
   - **Key**: `PEXELS_API_KEY`
   - **Value**: `5PDvDcvSRnnBe1zZvMoJPyfuDwZpdSwm5eBjabBrwztV4t38UueJ4Bdt`
6. Cliquez sur "Save Changes"
7. Redéployez le service pour appliquer les changements

## Configuration locale

La clé API est déjà configurée dans `/backend/.env` :
```
PEXELS_API_KEY=5PDvDcvSRnnBe1zZvMoJPyfuDwZpdSwm5eBjabBrwztV4t38UueJ4Bdt
```

## Scripts de seed modifiés

Les scripts suivants utilisent maintenant l'API Pexels pour les images :
- `seed_exercises.py` - 101 exercices
- `seed_shop.py` - 13 produits
- `seed_recipes.py` - 38 recettes
- `seed_blog.py` - 5 articles

## Service Pexels

Le service `/backend/api/services/pexels.py` inclut :
- Récupération d'images optimisées depuis Pexels API
- Fallback automatique vers Unsplash en cas d'erreur
- Fonctions spécifiques pour chaque type de contenu (exercices, produits, recettes, articles)
