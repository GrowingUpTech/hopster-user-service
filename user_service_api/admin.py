from django.contrib import admin
from user_service_api.models.user_token import UserToken
from user_service_api.models.user_nutrition import UserNutrition
from .custom_admin.custom_outstanding_token_admin import CustomOutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

admin.site.register(UserToken)
admin.site.register(UserNutrition)
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)