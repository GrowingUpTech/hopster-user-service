from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True