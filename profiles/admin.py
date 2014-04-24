from django.contrib import admin

from .models import UserPurchase, UserProfile


class UserPurchaseAdmin(admin.ModelAdmin):
    class Meta:
        model = UserPurchase

class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile

admin.site.register(UserPurchase, UserPurchaseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
