from django.contrib import admin

from .models import Product, Category, ProductImage, Tag, CategoryImage

# VERY IMPORTANT - These inlines need to go above the admin classes or they won't work
class TagInline(admin.TabularInline):
    prepopulated_fields = {"slug": ('tag',)} # automatically fills in the slug field when typing the tag in
    extra = 1 # this limits the number of tags to 1 by default (you can click to add more)
    model = Tag # connects the tag with the specific Product being created/edited

class ProductImageInline(admin.TabularInline):
    model = ProductImage # establishes the association between the product and the image and shows it in the admin panel

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage

# Admin components
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'current_price', 'categories') # this is where you decide on the columns to show in the product admin panel
    inlines = [TagInline, ProductImageInline] # sets up the two inline attribute selectors of tags and images
    search_fields = ['title', 'description', 'price', 'category__title', 'category__description', 'tag__tag'] # establishes what fields are searchable
    list_filter = ['price', 'timestamp', 'updated'] # establishes the filter process on the right hand side of the page
    prepopulated_fields = {"slug": ('title',)} # automatically creates the slug for the url from the product name while it's being typed in
    readonly_fields = ['timestamp','updated', 'categories'] # this shows the categories that the product has listed on the form page

    class Meta:
        model = Product # connects a variable 'model' to the product model

    def current_price(self, obj): # this is a method that takes in the product and returns either the sale or regular price
        if obj.sale_price > 0:
            return obj.sale_price
        else:
            return obj.price

    def categories(self, obj): # this categories method that enables the categories to be clickable
        cat_call = [] # great name for this variable, I think it should be appreciated
        for i in obj.category_set.all(): # iterates through the categories and converts each element in the array to a standard html link
            link = "<a href='/admin/products/category/" + str(i.id) + "'>" + i.title + "</a>"
            cat_call.append(link) # appends the html snippets to the array
        return ",".join(cat_call) # connects all of the items with a comma separating them

    categories.allow_tags = True # this function call allows for the categories column to allow html tags

admin.site.register(Product, ProductAdmin) # connects the product model with the productadmin page


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    inlines = [CategoryImageInline]
    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)
