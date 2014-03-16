from django.shortcuts import render_to_response, RequestContext, Http404


from .models import Product, Category, ProductImage
from .forms import ProductForm

def list_all(request):
    products = Product.objects.filter(active=True)
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def edit_product(request, slug):
    instance = Product.objects.get(slug=slug)
    # this conditional ensures that only the product owners can edit the product,
    # any other user trying to access the edit form will be shown a 404 error
    if request.user == instance.user:
        form = ProductForm(request.POST or None, instance=instance) # this performs a post request to make the edit work from the form

        if form.is_valid():
            product_edit = form.save(commit=False)

            product_edit.save()

        return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

def single(request, slug):
    product = Product.objects.get(slug=slug)

    images = product.productimage_set.all()

    categories = product.category_set.all()
    context = {
        "product": product,
        "categories": categories,
        "edit": True,
        "images": images,
    }

    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))
