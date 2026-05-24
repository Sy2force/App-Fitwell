# FitWell - Plateforme de Fitness et Wellness

FitWell est une application web complète pour le fitness et le wellness. Elle permet aux utilisateurs de suivre leurs entrainements, planifier leur nutrition, et progresser avec un systeme de gamification.

## Table des matieres

- Fonctionnalites
- Installation
- Structure du projet
- Base de donnees
- API
- Deploiement

## Fonctionnalites

### Onboarding
Les nouveaux utilisateurs passent par un processus d'integration en 4 etapes qui genere automatiquement leur premier plan personnalise. Ils selectionnent leur objectif (perte de poids, prise de masse, maintien), leur niveau d'activite, et leurs donnees biometriques.

### AI Planner
Le planificateur genere des programmes d'entrainement et de nutrition bases sur les donnees de l'utilisateur. Il calcule le BMR (taux metabolique de base), le TDEE (depense energetique totale), et les macros (proteines, glucides, lipides) en utilisant la formule Mifflin-St Jeor.

### Workout Tracking
Les utilisateurs peuvent enregistrer leurs sessions d'entrainement en temps reel. Ils ajoutent des series avec le nombre de repetitions et la charge. Le systeme calcule automatiquement le volume total et la duree de la session. Chaque session complete donne de l'experience (XP).

### Gamification
Le systeme de gamification inclut:
- XP et niveaux (chaque niveau necessite 500 XP de plus que le precedent)
- 20 badges a debloquer (entrainements, series, jalons, social)
- Series quotidiennes pour encourager la constance
- Classement global pour comparer les utilisateurs

### Analytics
Six graphiques interactifs montrent la progression de l'utilisateur: evolution du poids, volume par groupe musculaire, records personnels, frequence d'entrainement, score de constance, et progression XP.

### Dashboard
Le tableau de bord affiche le journal quotidien (eau, sommeil, humeur, poids), les statistiques hebdomadaires, l'agenda du jour, et les graphiques de progression.

### Nutrition
39 recettes avec macros detaillees sont disponibles. Les utilisateurs peuvent filtrer par categorie et niveau. Un calculateur BMI et macros est inclus.

### Blog
5 articles de qualite avec systeme de commentaires, likes, et categories.

### Programmes d'entrainement
3 programmes pre-configures (perte de poids, prise de masse, mobilite et yoga) avec structure detaillee.

### Boutique
13 produits (musculation, cardio, yoga, vetements, nutrition, accessoires) avec filtres par categorie.

### Panier et commandes
Systeme de panier fonctionnel avec gestion des quantites et processus de commande.

### Favoris
Les utilisateurs peuvent ajouter des exercices, recettes, et produits a leurs favoris avec des notes personnelles.

### Internationalisation
Support complet francais et anglais avec selecteur de langue dans la barre de navigation.

## Installation

### Prerequis
- Python 3.9 ou superieur
- pip
- Git

### 1. Cloner et installer

```bash
git clone https://github.com/Sy2force/App-Fitwell.git
cd fitwell

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r backend/requirements.txt
```

### 2. Configuration de la base de donnees

```bash
cd backend

python3 manage.py migrate

python3 manage.py seed_db          # Admin et categories
python3 manage.py seed_exercises   # 101 exercices
python3 manage.py seed_blog        # 5 articles
python3 manage.py seed_badges      # 20 badges
python3 manage.py seed_recipes     # 39 recettes
python3 manage.py seed_programs    # 3 programmes
python3 manage.py seed_shop        # 13 produits
python3 manage.py seed_demo_user   # Utilisateur demo

python3 manage.py compilemessages
```

### 3. Lancer le serveur

```bash
python3 manage.py runserver
```

Acces:
- Application: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/en/admin/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/

Compte admin (apres seed_db):
- Username: admin
- Password: adminpassword

## Structure du projet

```
fitwell/
├── backend/                    # Application Django
│   ├── api/                    # API REST et modeles
│   │   ├── models/             # Modeles de donnees
│   │   ├── views/              # ViewSets API
│   │   ├── serializers/        # Serializers
│   │   ├── services/           # Services metier
│   │   ├── management/         # Commandes seed
│   │   └── tests/              # Tests unitaires
│   ├── web/                    # Frontend Django
│   │   ├── views/              # Vues
│   │   ├── templates/          # Templates HTML
│   │   ├── static/             # CSS et JavaScript
│   │   └── forms.py            # Formulaires Django
│   ├── config/                 # Configuration
│   │   ├── settings.py         # Settings Django
│   │   └── urls.py             # URLs racine
│   ├── locale/                 # Traductions FR/EN
│   ├── manage.py               # CLI Django
│   ├── requirements.txt        # Dependances Python
│   └── build.sh                # Script build Render
└── README.md                   # Ce fichier
```

## Modeles de donnees

### User et Stats
- User (utilisateur custom avec AbstractUser)
- UserStats (XP, niveaux, series, scores)

### Contenu
- Category, Article, Comment

### Entrainement
- Exercise, WorkoutSession, ExerciseSet

### Nutrition
- Recipe

### Planning
- WellnessPlan, DailyLog, CustomEvent

### Programmes
- Program, ProgramDay, ProgramExercise, UserProgramProgress

### Boutique
- Product, Cart, CartItem, Order, OrderItem

### Favoris
- Favorite (polymorphique: exercise, recipe, product)

### Gamification
- Badge, UserBadge

## Base de donnees peuplee

- 101 exercices (tous les groupes musculaires)
- 39 recettes (avec macros detaillees)
- 20 badges (systeme de recompenses)
- 5 articles (contenu blog)
- 3 programmes (perte de poids, prise de masse, mobilite et yoga)
- 13 produits (boutique sport)
- 9 utilisateurs (dont admin et demo)

## API

### Documentation
- Browsable API DRF: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

### Authentification (JWT)

| Methode | Endpoint | Description |
|---|---|---|
| POST | /api/register/ | Inscription d'un nouvel utilisateur |
| POST | /api/token/ | Connexion: retourne access et refresh |
| POST | /api/token/refresh/ | Rafraichir le token d'acces |

### Articles

| Methode | Endpoint | Description | Permission |
|---|---|---|---|
| GET | /api/articles/ | Liste paginee des articles | Anonyme OK |
| GET | /api/articles/?search= | Recherche par titre, contenu ou tag | Anonyme OK |
| GET | /api/articles/?tags__name= | Filtre par tag | Anonyme OK |
| GET | /api/articles/?ordering= | Tri par auteur | Anonyme OK |
| GET | /api/articles/<id>/ | Detail d'un article et ses commentaires | Anonyme OK |
| POST | /api/articles/ | Creer un article | Authentifie |
| PUT/PATCH | /api/articles/<id>/ | Modifier un article | Auteur uniquement |
| DELETE | /api/articles/<id>/ | Supprimer un article | Auteur uniquement |

### Commentaires

| Methode | Endpoint | Description | Permission |
|---|---|---|---|
| GET | /api/articles/<id>/comments/ | Liste des commentaires d'un article | Anonyme OK |
| POST | /api/articles/<id>/comments/ | Poster un commentaire | Authentifie |
| DELETE | /api/comments/<id>/ | Supprimer son commentaire | Auteur uniquement |

### Tags

| Methode | Endpoint | Description |
|---|---|---|
| GET | /api/tags/ | Liste de tous les tags |
| GET | /api/tags/?search= | Recherche tag par nom |

### Modeles de donnees

| Modele | Champs cles | Relations |
|---|---|---|
| User | username (unique), email (unique), password | articles, comments |
| Article | title, content, created_at (auto), updated_at (auto) | FK author, M2M tags, M2M likes, FK category |
| Comment | content, created_at (auto) | FK article, FK author, M2M tags |
| Tag | name (unique), slug (auto) | M2M articles, M2M comments |

## Deploiement

### Variables d'environnement

Creer .env a la racine:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Deploiement Render

1. Push sur GitHub
```bash
git push origin main
```

2. Render Dashboard
   - https://dashboard.render.com
   - New + -> Web Service
   - Repository: Sy2force/App-Fitwell
   - Branch: main
   - Root Directory: backend
   - Build Command: ./build.sh
   - Start Command: gunicorn config.wsgi:application --log-file - --capture-output --log-level debug

3. Variables d'environnement
   - PYTHON_VERSION: 3.11.9
   - DEBUG: False
   - RENDER: True
   - SECRET_KEY: (genere automatiquement)
   - ALLOWED_HOSTS: .onrender.com
   - CSRF_TRUSTED_ORIGINS: https://.onrender.com

4. Base de donnees
   - Creer une base de donnees PostgreSQL
   - Connecter DATABASE_URL

5. Attendre 5-10 minutes pour le deploiement

## Commandes utiles

### Developpement

```bash
# Demarrer serveur
python3 manage.py runserver

# Tests
python3 manage.py test

# Verifications
python3 manage.py check

# Shell Django
python3 manage.py shell
```

### Base de donnees

```bash
# Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Seed data
python3 manage.py seed_db
python3 manage.py seed_exercises
python3 manage.py seed_recipes
python3 manage.py seed_badges
python3 manage.py seed_blog

# Creer superuser
python3 manage.py createsuperuser
```

### Internationalisation

```bash
# Extraire messages
python3 manage.py makemessages -l en

# Compiler messages
python3 manage.py compilemessages
```

### Production

```bash
# Collecter static files
python3 manage.py collectstatic

# Verifier deploiement
python3 manage.py check --deploy
```

## Statistiques du projet

### Code
- 80+ fichiers Python
- 40+ templates HTML
- 2 CSS + 7 JavaScript
- 9000+ lignes de code

### Base de donnees
- 18 modeles de donnees
- 20+ relations
- 200+ entrees seed

### Tests
- 23 tests unitaires
- 31 tests E2E
- 30 verifications systeme

## Technologies utilisees

- Django 4.2 - Framework web Python
- Django REST Framework - API REST
- TailwindCSS - Framework CSS
- Chart.js - Graphiques interactifs
- PostgreSQL - Base de donnees
- Gunicorn - WSGI server
- WhiteNoise - Static files
- Playwright - Tests E2E

## License

MIT License - Voir LICENSE

## A propos

FitWell est une plateforme complete de fitness et wellness developpee avec Django. Elle inclut un coach AI avec interface futuriste, une gamification complete, un planificateur AI pour des plans personnalises, des analytics avancees, et une internationalisation FR/EN complete.

Statut: Production Ready - 100% Complet
