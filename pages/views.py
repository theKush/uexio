from django.shortcuts import render_to_response, RequestContext

from products.models import Product

def index(request):
    # newest 6 created listings can go here OR we can have featured products
    products = Product.listing().filter(featured=True)[:6]
    return render_to_response("pages/index.html", locals(), context_instance=RequestContext(request))
