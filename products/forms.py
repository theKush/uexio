from django.forms import ModelForm # this is a built in django form call that allows us to directly edit model data

from .models import Product, ProductImage, Comment, Coupon # this is a call to a relative model, it just needs the '.' because we're already in the product dir

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'sale_price', 'isbn_number', 'author')

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('title', 'image', 'featured_image')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('code', 'discount')
