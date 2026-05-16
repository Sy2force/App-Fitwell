#!/usr/bin/env bash
# ==============================================================================
# Script de build FitWell pour Render
# Exécuté avec rootDir=backend, donc le pwd est déjà /backend
# ==============================================================================
set -o errexit

echo "==> [1/6] Installation des dépendances..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "==> [2/6] Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "==> [3/6] Compilation des traductions (si gettext disponible)..."
python manage.py compilemessages || echo "Info: compilemessages skipped (gettext absent)"

echo "==> [4/6] Migrations base de données..."
python manage.py migrate --noinput

echo "==> [5/6] Seeding (idempotent)..."
python manage.py seed_db || echo "Info: seed_db a échoué (peut-être déjà fait)"
python manage.py seed_badges || echo "Info: seed_badges a échoué"
python manage.py seed_assignment || echo "Info: seed_assignment a échoué"

echo "==> [6/6] Garantir des images uniques (articles/recettes/exercices)..."
python manage.py fix_unique_images || echo "Info: fix_unique_images a échoué"

echo "==> Build terminé avec succès."
