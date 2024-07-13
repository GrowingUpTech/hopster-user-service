from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from user_service_api.models.user_nutrition import UserNutrition
from user_service_api.serializers.user_nutrition_serializers import UserNutritionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_nutrition(request):
    username = request.data.get('username')
    food_nutrition_data = request.data.get('food_nutrition_data')

    # Fetch User by username
    user = get_object_or_404(User, username=username)

    # Create UserNutrition instance
    serializer = UserNutritionSerializer(
        data={
        'user': user.id,
        'food_name': food_nutrition_data['food_name'],
        'food_tag': food_nutrition_data['food_tag'],
        'food_kcal': food_nutrition_data['food_kcal'],
        'food_carbohydrates': food_nutrition_data['food_carbohydrates'],
        'food_protein': food_nutrition_data['food_protein'],
        'food_fat': food_nutrition_data['food_fat'],
    })

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_meal_by_date(request):
    username = request.data.get('username')
    today = timezone.now().date()
    
    user = get_object_or_404(User, username=username)

    user_meals_today = UserNutrition.objects.filter(user=user.id, datetime__date=today)
    serializer = UserNutritionSerializer(user_meals_today, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

