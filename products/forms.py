from django.forms import ModelForm # this is a built in django form call that allows us to directly edit model data

from .models import Product # this is a call to a relative model, it just needs the '.' because we're already in the product dir

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'sale_price', 'isbn_number', 'author')
