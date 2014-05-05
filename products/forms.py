from django.forms import ModelForm # this is a built in django form call that allows us to directly edit model data
from django.forms import ValidationError
from django.forms.models import BaseModelFormSet, modelformset_factory

from .models import Product, ProductImage, Comment, Coupon # this is a call to a relative model, it just needs the '.' because we're already in the product dir

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'author', 'isbn_number', 'headline', 'description', 'condition', 'price', 'download')

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('title', 'image', 'featured_image')

class BaseProductImageFormSet(BaseModelFormSet):
    def clean(self):
        super(BaseProductImageFormSet, self).clean()

        # Exactly one image should be marked as featured.
        featured = sum(form.cleaned_data.get('featured_image', False)
                       for form in self.forms
                       if form not in self.deleted_forms)
        if featured == 0:
            raise ValidationError('At least one image needs to be featured.')
        elif featured > 1:
            raise ValidationError('Only one image can be featured.')

ProductImageFormSet = modelformset_factory(ProductImage,
                                           form=ProductImageForm,
                                           formset=BaseProductImageFormSet,
                                           can_delete=True)


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
