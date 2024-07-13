from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserNutrition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    food_name = models.CharField(max_length=255, null=False, default="null")
    food_tag = models.CharField(max_length=2, null=False, default="null")  # Store FoodTag as CharField
    food_kcal = models.FloatField(default=0)
    food_carbohydrates = models.FloatField(default=0)
    food_protein = models.FloatField(default=0)
    food_fat = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.food_name} at {self.datetime}'