from django.db import models
from django.utils.text import slugify
from .user import User

# -----------------------------------------------------------------------------
# TAGS
# -----------------------------------------------------------------------------
class Tag(models.Model):
    """
    Free tags attached to an Article or Comment.
    Allows filtering/searching content by topic (e.g. 'python', 'fitness').
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# -----------------------------------------------------------------------------
# CATEGORIES
# -----------------------------------------------------------------------------
class Category(models.Model):
    """
    Blog themes (e.g. Nutrition, Strength, Mental).
    Slug is auto-generated if not filled.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# -----------------------------------------------------------------------------
# ARTICLES
# -----------------------------------------------------------------------------
class Article(models.Model):
    """
    The core of the content.
    Each article has an author, a category and an image.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = models.TextField()
    image = models.CharField(max_length=500, blank=True, null=True) # Changed to CharField for URL support
    is_published = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    
    # Auto-managed dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto generation of slug (URL friendly) from title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# -----------------------------------------------------------------------------
# COMMENTS
# -----------------------------------------------------------------------------
class Comment(models.Model):
    """
    User reactions under an article.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
