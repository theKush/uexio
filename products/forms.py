from django.forms import ModelForm # this is a built in django form call that allows us to directly edit model data
from django.forms import ValidationError
from django.forms.models import BaseModelFormSet, modelformset_factory

from .models import Product, ProductImage, Comment, Coupon # this is a call to a relative model, it just needs the '.' because we're already in the product dir
# create new product form
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'author', 'isbn_number', 'headline', 'category', 'description', 'condition', 'price', 'download')
# product images form
class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('title', 'image', 'featured_image')
# making sure that featured images are set, and only one featured image is allowed.
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

# form to add comments on single product pages
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
# form to create coupon codes and making sure coupon discount is less than the product price
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
