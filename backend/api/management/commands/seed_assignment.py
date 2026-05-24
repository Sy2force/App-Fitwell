"""
Minimal seed compliant with the Django final project specification.

Creates:
- 2 users (alice, bob)
- 2 articles with tags
- 2 comments per article (with tags)

Idempotent: can be rerun without duplicates.
"""
from django.core.management.base import BaseCommand
from api.models import User, Article, Comment, Tag, Category


# Seed data compliant with spec: 2 users, 2 articles, 2 comments/article
USERS = [
    {"username": "alice", "email": "alice@example.com", "password": "alicepass123"},
    {"username": "bob", "email": "bob@example.com", "password": "bobpass123"},
]

ARTICLES = [
    {
        "title": "Discovering Django REST Framework",
        "content": (
            "Django REST Framework is a powerful toolkit for building "
            "Web APIs. This article introduces key concepts: serializers, "
            "viewsets, routers and permissions."
        ),
        "author_username": "alice",
        "tags": ["python", "django", "api"],
    },
    {
        "title": "Why adopt PostgreSQL in production",
        "content": (
            "PostgreSQL offers reliability, performance and advanced features "
            "(JSONB, full-text search, transactions) making it an ideal choice "
            "for serious Django applications."
        ),
        "author_username": "bob",
        "tags": ["postgresql", "database", "production"],
    },
]

COMMENTS = {
    "Discovering Django REST Framework": [
        {"author": "bob", "content": "Excellent reminder about viewsets, thanks!", "tags": ["python", "feedback"]},
        {"author": "alice", "content": "I would add a word about Throttles in v2.", "tags": ["api"]},
    ],
    "Why adopt PostgreSQL in production": [
        {"author": "alice", "content": "PostgreSQL full-text search is underrated.", "tags": ["postgresql", "search"]},
        {"author": "bob", "content": "Combine with pgbouncer for high loads.", "tags": ["production"]},
    ],
}


class Command(BaseCommand):
    help = "Minimal seed compliant with specification (2 users, 2 articles, 2 comments/article)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding assignment data..."))

        # Default category (optional, article can do without)
        default_cat, _ = Category.objects.get_or_create(name="General")

        # 1. Users
        users = {}
        for u in USERS:
            user, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            if created or not user.has_usable_password():
                user.set_password(u["password"])
                user.save()
                self.stdout.write(f"  + user created: {user.username}")
            else:
                self.stdout.write(f"  = existing user: {user.username}")
            users[u["username"]] = user

        # 2. Articles with tags
        articles_by_title = {}
        for a in ARTICLES:
            article, created = Article.objects.get_or_create(
                title=a["title"],
                defaults={
                    "author": users[a["author_username"]],
                    "category": default_cat,
                    "content": a["content"],
                },
            )
            # Tags: list comprehension to retrieve/create in batch
            tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in a["tags"]]
            article.tags.set(tag_objs)
            articles_by_title[a["title"]] = article
            verb = "created" if created else "existing"
            self.stdout.write(f"  + article {verb}: {article.title} (tags: {a['tags']})")

        # 3. Comments with tags (2 per article)
        for title, comments in COMMENTS.items():
            article = articles_by_title[title]
            for c in comments:
                comment, created = Comment.objects.get_or_create(
                    article=article,
                    author=users[c["author"]],
                    content=c["content"],
                )
                tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in c["tags"]]
                comment.tags.set(tag_objs)
                if created:
                    self.stdout.write(f"    > comment by {c['author']} on '{title[:30]}...' (tags: {c['tags']})")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nOK: {User.objects.count()} users, "
                f"{Article.objects.count()} articles, "
                f"{Comment.objects.count()} comments, "
                f"{Tag.objects.count()} tags."
            )
        )
