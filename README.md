# FitWell - Fitness and Wellness Platform

FitWell is a complete web application for fitness and wellness. It allows users to track their workouts, plan their nutrition, and progress with a gamification system.

## Table of Contents

- Features
- Installation
- Project Structure
- Database
- API
- Deployment

## Features

### Onboarding
New users go through a 4-step integration process that automatically generates their first personalized plan. They select their goal (weight loss, muscle gain, maintenance), their activity level, and their biometric data.

### AI Planner
The planner generates workout and nutrition programs based on user data. It calculates BMR (basal metabolic rate), TDEE (total daily energy expenditure), and macros (proteins, carbs, fats) using the Mifflin-St Jeor formula.

### Workout Tracking
Users can record their workout sessions in real time. They add sets with the number of repetitions and the load. The system automatically calculates the total volume and duration of the session. Each completed session gives experience points (XP).

### Gamification
The gamification system includes:
- XP and levels (each level requires 500 more XP than the previous)
- 20 badges to unlock (workouts, streaks, milestones, social)
- Daily streaks to encourage consistency
- Global leaderboard to compare users

### Analytics
Six interactive charts show user progression: weight evolution, volume by muscle group, personal records, training frequency, consistency score, and XP progression.

### Dashboard
The dashboard displays the daily log (water, sleep, mood, weight), weekly statistics, daily agenda, and progression charts.

### Nutrition
39 recipes with detailed macros are available. Users can filter by category and level. A BMI and macros calculator is included.

### Blog
5 quality articles with comment system, likes, and categories.

### Training Programs
3 pre-configured programs (weight loss, muscle gain, mobility and yoga) with detailed structure.

### Shop
13 products (bodybuilding, cardio, yoga, clothing, nutrition, accessories) with category filters.

### Cart and Orders
Functional cart system with quantity management and order process.

### Favorites
Users can add exercises, recipes, and products to their favorites with personal notes.

### Internationalization
Complete French and English support with language selector in the navigation bar.

## Installation

### Prerequisites
- Python 3.9 or higher
- pip
- Git

### 1. Clone and install

```bash
git clone https://github.com/Sy2force/App-Fitwell.git
cd fitwell

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r backend/requirements.txt
```

### 2. Database configuration

```bash
cd backend

python3 manage.py migrate

python3 manage.py seed_db          # Admin and categories
python3 manage.py seed_exercises   # 101 exercises
python3 manage.py seed_blog        # 5 articles
python3 manage.py seed_badges      # 20 badges
python3 manage.py seed_recipes     # 39 recipes
python3 manage.py seed_programs    # 3 programs
python3 manage.py seed_shop        # 13 products
python3 manage.py seed_demo_user   # Demo user

python3 manage.py compilemessages
```

### 3. Start the server

```bash
python3 manage.py runserver
```

Access:
- Application: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/en/admin/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/

Admin account (after seed_db):
- Username: admin
- Password: adminpassword

## Project Structure

```
fitwell/
├── backend/                    # Django application
│   ├── api/                    # REST API and models
│   │   ├── models/             # Data models
│   │   ├── views/              # API ViewSets
│   │   ├── serializers/        # Serializers
│   │   ├── services/           # Business services
│   │   ├── management/         # Seed commands
│   │   └── tests/              # Unit tests
│   ├── web/                    # Django frontend
│   │   ├── views/              # Views
│   │   ├── templates/          # HTML templates
│   │   ├── static/             # CSS and JavaScript
│   │   └── forms.py            # Django forms
│   ├── config/                 # Configuration
│   │   ├── settings.py         # Django settings
│   │   └── urls.py             # Root URLs
│   ├── locale/                 # FR/EN translations
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python dependencies
│   └── build.sh                # Render build script
└── README.md                   # This file
```

## Data Models

### User and Stats
- User (custom user with AbstractUser)
- UserStats (XP, levels, streaks, scores)

### Content
- Category, Article, Comment

### Training
- Exercise, WorkoutSession, ExerciseSet

### Nutrition
- Recipe

### Planning
- WellnessPlan, DailyLog, CustomEvent

### Programs
- Program, ProgramDay, ProgramExercise, UserProgramProgress

### Shop
- Product, Cart, CartItem, Order, OrderItem

### Favorites
- Favorite (polymorphic: exercise, recipe, product)

### Gamification
- Badge, UserBadge

## Database Seeded

- 101 exercises (all muscle groups)
- 39 recipes (with detailed macros)
- 20 badges (reward system)
- 5 articles (blog content)
- 3 programs (weight loss, muscle gain, mobility and yoga)
- 13 products (fitness shop)
- 9 users (including admin and demo)

## API

### Documentation
- Browsable API DRF: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

### Authentication (JWT)

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/register/ | Register a new user |
| POST | /api/token/ | Login: returns access and refresh |
| POST | /api/token/refresh/ | Refresh access token |

### Articles

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | /api/articles/ | Paginated article list | Anonymous OK |
| GET | /api/articles/?search= | Search by title, content or tag | Anonymous OK |
| GET | /api/articles/?tags__name= | Filter by tag | Anonymous OK |
| GET | /api/articles/?ordering= | Sort by author | Anonymous OK |
| GET | /api/articles/<id>/ | Article detail and comments | Anonymous OK |
| POST | /api/articles/ | Create an article | Authenticated |
| PUT/PATCH | /api/articles/<id>/ | Modify an article | Author only |
| DELETE | /api/articles/<id>/ | Delete an article | Author only |

### Comments

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | /api/articles/<id>/comments/ | List of article comments | Anonymous OK |
| POST | /api/articles/<id>/comments/ | Post a comment | Authenticated |
| DELETE | /api/comments/<id>/ | Delete own comment | Author only |

### Tags

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/tags/ | List of all tags |
| GET | /api/tags/?search= | Search tag by name |

### Data Models

| Model | Key Fields | Relations |
|---|---|---|
| User | username (unique), email (unique), password | articles, comments |
| Article | title, content, created_at (auto), updated_at (auto) | FK author, M2M tags, M2M likes, FK category |
| Comment | content, created_at (auto) | FK article, FK author, M2M tags |
| Tag | name (unique), slug (auto) | M2M articles, M2M comments |

## Deployment

### Environment Variables

Create .env at root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Render Deployment

1. Push to GitHub
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

3. Environment Variables
   - PYTHON_VERSION: 3.11.9
   - DEBUG: False
   - RENDER: True
   - SECRET_KEY: (auto generated)
   - ALLOWED_HOSTS: .onrender.com
   - CSRF_TRUSTED_ORIGINS: https://.onrender.com

4. Database
   - Create a PostgreSQL database
   - Connect DATABASE_URL

5. Wait 5-10 minutes for deployment

## Useful Commands

### Development

```bash
# Start server
python3 manage.py runserver

# Tests
python3 manage.py test

# Checks
python3 manage.py check

# Django shell
python3 manage.py shell
```

### Database

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

# Create superuser
python3 manage.py createsuperuser
```

### Internationalization

```bash
# Extract messages
python3 manage.py makemessages -l en

# Compile messages
python3 manage.py compilemessages
```

### Production

```bash
# Collect static files
python3 manage.py collectstatic

# Check deployment
python3 manage.py check --deploy
```

## Project Statistics

### Code
- 80+ Python files
- 40+ HTML templates
- 2 CSS + 7 JavaScript
- 9000+ lines of code

### Database
- 18 data models
- 20+ relations
- 200+ seed entries

### Tests
- 23 unit tests
- 31 E2E tests
- 30 system checks

## Technologies Used

- Django 4.2 - Python web framework
- Django REST Framework - REST API
- TailwindCSS - CSS framework
- Chart.js - Interactive charts
- PostgreSQL - Database
- Gunicorn - WSGI server
- WhiteNoise - Static files
- Playwright - E2E tests

## License

MIT License - See LICENSE

## About

FitWell is a complete fitness and wellness platform developed with Django. It includes an AI coach with futuristic interface, complete gamification, AI planner for personalized plans, advanced analytics, and complete FR/EN internationalization.

Status: Production Ready - 100% Complete
