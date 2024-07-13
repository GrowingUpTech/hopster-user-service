from rest_framework import serializers
from user_service_api.models.user_nutrition import UserNutrition

class UserNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNutrition
        fields = ['user', 'datetime', 'food_name', 'food_tag', 'food_kcal', 'food_carbohydrates', 'food_protein', 'food_fat']
        read_only_fields = ['datetime']

