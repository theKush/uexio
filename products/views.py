from django.shortcuts import render_to_response, RequestContext, Http404


from .models import Product, Category

def list_all(request):
    products = Product.objects.filter(active=True)
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def single(request):
    product = Product.objects.all()[0]
    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))
