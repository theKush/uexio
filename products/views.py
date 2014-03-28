from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory


from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageForm

def list_all(request):
    products = Product.objects.filter(active=True)
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def add_product(request):
        form = ProductForm(request.POST or None)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(form.cleaned_data['title'])
            product.active = False
            product.save()
            return HttpResponseRedirect('/products/%s'%(product.slug))
        return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))


def manage_product_image(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except:
        product = False

    if request.user == product.user:
        queryset = ProductImage.objects.filter(product__slug=slug) # this queries the images and ensures that the correct image is selected
        ProductImageFormset = modelformset_factory(ProductImage, form=ProductImageForm, can_delete=True)
        formset = ProductImageFormset(request.POST or None, request.FILES or None, queryset=queryset)
        form = ProductImageForm(request.POST or None) # this initializes the ability to reference the image for the product

        # validates and saves the image when uploaded
        if formset.is_valid(): #
            for form in formset:
                instance = form.save(commit=False)
                instance.save()

        return render_to_response("products/manage_images.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404


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
