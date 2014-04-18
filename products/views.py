import os

from mimetypes import guess_type

from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageForm

def list_all(request):
    title = "All Products"
    products = Product.objects.filter(active=True)
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def download_product(request, slug, filename):
    product = Product.objects.get(slug=slug)

    if not request.user.has_purchased(product):
        raise Http404

    product_file = str(product.download)
    file_path = os.path.join(settings.PROTECTED_UPLOADS, product_file)
    wrapper = FileWrapper(file(file_path))
    response = HttpResponse(wrapper, content_type=guess_type(product_file))

    # these are the content headers for the download
    response['Content-Diposition'] = 'attachement;filename=%s' %filename
    response['Content-Type'] = ''
    response['X-SendFile'] = file_path
    return response

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
    product = Product.objects.get(slug=slug)

    if request.user != product.user:
        raise Http404

    # this queries the images and ensures that the correct image is selected
    queryset = ProductImage.objects.filter(product__slug=slug)
    ProductImageFormset = modelformset_factory(ProductImage, form=ProductImageForm, can_delete=True)
    formset = ProductImageFormset(request.POST or None, request.FILES or None, queryset=queryset)

    if request.method == 'POST':
        try:
            # all images are automatically validated during save()
            images = formset.save(commit=False)
            for image in images:
                image.product = product
                image.save()
            return HttpResponseRedirect(reverse('manage_product_image', args=[product.slug]))
        except ValueError: # handle validation errors
            pass

    return render_to_response("products/manage_images.html", locals(), context_instance=RequestContext(request))

def edit_product(request, slug):
    instance = Product.objects.get(slug=slug)
    # this conditional ensures that only the product owners can edit the product,
    # any other user trying to access the edit form will be shown a 404 error
    if request.user != instance.user:
        raise Http404

    form = ProductForm(request.POST or None, instance=instance) # this performs a post request to make the edit work from the form

    if form.is_valid():
        product_edit = form.save(commit=False)
        product_edit.save()

    return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))

def single(request, slug):
    product = Product.objects.get(slug=slug)
    images = product.productimage_set.all()
    categories = product.category_set.all()

    if request.user.is_authenticated():
        downloadable = request.user.has_purchased(product)

    edit = True

    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

def search_products(request):
    query = request.GET['query']
    products = Product.objects.filter(Q(description__contains=query) | Q(title__contains=query) | Q(author__contains=query), active=True)
    title = "Products matching " + query

    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def activate_product(request, slug):
    product = Product.objects.get(slug=slug)
    product.active = True
    product.save()
    return HttpResponseRedirect(reverse('listings'))

def deactivate_product(request, slug):
    product = Product.objects.get(slug=slug)
    product.active = False
    product.save()
    return HttpResponseRedirect(reverse('listings'))
