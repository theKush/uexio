from django.contrib import admin

from .models import Product, Category, ProductImage, Tag

class TagInline(admin.TabularInline):
    model = Tag

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'current_price', 'categories')
    inlines = [TagInline, ProductImageInline]
    search_fields = ['title', 'description', 'price', 'category__title', 'category__description', 'tag__tag']
    list_filter = ['price', 'timestamp', 'updated']

    class Meta:
        model = Product

    def current_price(self, obj):
        if obj.sale_price > 0:
            return obj.sale_price
        else:
            return obj.price

    def categories(self, obj):
        cat_call = []
        for i in obj.category_set.all():
            link = "<a href='/admin/products/category/" + str(i.id) + "'>" + i.title + "</a>"
            cat_call.append(link)
        return ",".join(cat_call)

    categories.allow_tags = True

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)
