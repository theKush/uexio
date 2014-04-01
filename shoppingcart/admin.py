from django.contrib import admin

from .models import Shoppingcart, ShoppingcartItem

class ShoppingcartItemInline(admin.TabularInline):
    model = ShoppingcartItem


class ShoppingcartAdmin(admin.ModelAdmin):
    inlines = [ShoppingcartItemInline]

    class Meta:
        model = Shoppingcart

admin.site.register(Shoppingcart, ShoppingcartAdmin)
