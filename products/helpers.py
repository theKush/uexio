from django.core.urlresolvers import reverse

def product_url(product):
    return reverse('single_product', args=[product.id, product.slug])
