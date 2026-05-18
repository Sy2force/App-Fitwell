from rest_framework import serializers
from api.models.favorite import Favorite
from api.models.workout import Exercise
from api.models.nutrition import Recipe
from api.models.shop import Product
from .workout import ExerciseSerializer
from .content import RecipeSerializer
from .shop import ProductSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    content_name = serializers.ReadOnlyField()
    
    # Dynamic content field based on content_type
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True, required=False)
    recipe_detail = RecipeSerializer(source='recipe', read_only=True, required=False)
    product_detail = ProductSerializer(source='product', read_only=True, required=False)

    class Meta:
        model = Favorite
        fields = [
            'id', 'user', 'content_type', 'exercise', 'recipe', 'product',
            'notes', 'created_at', 'content_name',
            'exercise_detail', 'recipe_detail', 'product_detail'
        ]
        read_only_fields = ['user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Only include the relevant detail field based on content_type
        content_type = instance.content_type
        if content_type == 'exercise':
            data.pop('recipe_detail', None)
            data.pop('product_detail', None)
        elif content_type == 'recipe':
            data.pop('exercise_detail', None)
            data.pop('product_detail', None)
        elif content_type == 'product':
            data.pop('exercise_detail', None)
            data.pop('recipe_detail', None)
        return data
