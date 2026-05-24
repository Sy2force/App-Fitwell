from rest_framework import serializers
from api.models import Article, Comment, Category, Tag, Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for nutrition recipes."""

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('slug', 'created_at')


class TagSerializer(serializers.ModelSerializer):
    """Simple serializer to expose tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagsRelatedField(serializers.Field):
    """
    Custom M2M field for Tags:
    - read: list of names ['python', 'fitness']
    - write: accepts a list of names (auto-creation if non-existent)
    This avoids the user having to manipulate IDs.
    """

    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("`tags` must be a list of names.")
        tags = []
        for raw in data:
            name = str(raw).strip().lower()
            if not name:
                continue
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        return tags


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tags = TagsRelatedField(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'author', 'author_username', 'content', 'tags', 'created_at')
        read_only_fields = ('author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        comment = Comment.objects.create(**validated_data)
        if tags:
            comment.tags.set(tags)
        return comment

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    image_url = serializers.CharField(source='image', required=False, allow_null=True)
    tags = TagsRelatedField(required=False)

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'slug', 'author', 'author_username',
            'category', 'category_name', 'category_slug',
            'content', 'image_url', 'tags',
            'is_published', 'created_at', 'updated_at',
            'comments', 'likes_count', 'is_liked',
        )
        read_only_fields = ('author', 'slug')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        if tags:
            article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
