from django.contrib import admin
from .models import UserToken
from .custom_admin.custom_outstanding_token_admin import CustomOutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

admin.site.register(UserToken)
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)