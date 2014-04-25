from django.forms import ModelForm # this is a built in django form call that allows us to directly edit model data
from django.forms import ValidationError

from .models import Product, ProductImage, Comment, Coupon # this is a call to a relative model, it just needs the '.' because we're already in the product dir

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'headline', 'description', 'condition', 'price', 'download')

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
        fields = ('product', 'code', 'discount')

    def clean_discount(self):
        discount = self.cleaned_data['discount']

        if 'product' in self.cleaned_data:
            product = self.cleaned_data['product']

            if discount >= product.price:
                raise ValidationError("Discount should be lower than price.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return discount
