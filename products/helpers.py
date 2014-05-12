from django.core.urlresolvers import reverse
# added product id's in the single product url along with the product slug
def product_url(product):
    return reverse('single_product', args=[product.id, product.slug])
