from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Article, Category, Comment, Tag, Recipe
from api.serializers import ArticleSerializer, CategorySerializer, CommentSerializer, TagSerializer, RecipeSerializer
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists recipes from the nutrition database.
    Read only (recipes are managed by seeds).
    URL: /api/recipes/
    Filters: ?category=lunch&difficulty=easy
    Search: ?search=protein
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty']
    search_fields = ['title', 'ingredients']
    ordering_fields = ['title', 'calories', 'prep_time_minutes', 'created_at']
    ordering = ['-created_at']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists available tags. Read only (tags are created
    automatically when creating articles/comments).
    URL: /api/tags/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    pagination_class = None

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Simple list of categories.
    Can sort or search by name.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'])
    def articles(self, request, slug=None):
        """
        Retrieves articles from a specific category.
        URL: /api/categories/{slug}/articles/
        """
        category = self.get_object()
        articles = Article.objects.filter(category=category).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Main API for articles.
    - Read: everyone (including anonymous).
    - Create: any authenticated user.
    - Modify / Delete: only the author (or admin).
    """
    # Load author and category directly to avoid 50 SQL queries
    queryset = (Article.objects
                .select_related('author', 'category')
                .prefetch_related('comments', 'tags')
                .order_by('-created_at'))
    serializer_class = ArticleSerializer
    # Requirements: authenticated user can create,
    # only the author (or admin) can modify/delete.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Filters: by category, author, tag, text search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'category__slug', 'tags__name', 'tags__slug']
    search_fields = ['title', 'content', 'tags__name']
    ordering_fields = ['created_at', 'title', 'author__username']

    def perform_create(self, serializer):
        # Automatically assign the author to the connected user
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Action to like/unlike an article.
        URL: /api/articles/{id}/like/
        """
        article = self.get_object()
        user = request.user
        
        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
            return Response({'status': 'unliked', 'likes_count': article.likes.count()})
        else:
            article.likes.add(user)
            return Response({'status': 'liked', 'likes_count': article.likes.count()})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Retrieves articles from the connected user.
        URL: /api/blog/articles/me/
        """
        articles = Article.objects.filter(author=request.user).order_by('-created_at')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        """
        Manages comments of a specific article (List / Create).
        URL: /api/articles/{id}/comments/
        """
        article = self.get_object()
        
        if request.method == 'GET':
            comments = article.comments.all().order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Inject the article via the URL (nested route)
            data = {**request.data, 'article': article.id}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, article=article)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment management on articles.
    Same logic: you can only modify YOUR comments.
    """
    queryset = (Comment.objects
                .select_related('author', 'article')
                .prefetch_related('tags')
                .order_by('-created_at'))
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['article', 'author', 'tags__name', 'tags__slug']
    search_fields = ['content', 'tags__name']
    ordering_fields = ['created_at', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
