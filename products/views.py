import os

from mimetypes import guess_type

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Product, Category, ProductImage, Comment, Coupon
from .forms import ProductForm, ProductImageForm, CommentForm, CouponForm, ProductImageFormSet

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
    form = ProductForm(request.POST or None, request.FILES or None)
    image_form = ProductImageForm(request.POST or None, request.FILES or None)

    if form.is_valid() and image_form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.slug = slugify(form.cleaned_data['title'])
        product.active = False
        product.save()
        image = image_form.save(commit=False)
        image.product = product
        image.featured_image = True
        image.save()
        return HttpResponseRedirect('/products/%s'%(product.slug))

    return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))

def manage_product_image(request, slug):
    product = Product.objects.get(slug=slug)

    if request.user != product.user:
        raise Http404

    # this queries the images and ensures that the correct image is selected
    queryset = ProductImage.objects.filter(product__slug=slug)
    formset = ProductImageFormSet(request.POST or None, request.FILES or None, queryset=queryset)

    if request.method == 'POST' and formset.is_valid():
        images = formset.save(commit=False)
        for image in images:
            image.product = product
            image.save()
        return HttpResponseRedirect(reverse('manage_product_image', args=[product.slug]))

    return render_to_response("products/manage_images.html", locals(), context_instance=RequestContext(request))

def edit_product(request, slug):
    instance = Product.objects.get(slug=slug)
    # this conditional ensures that only the product owners can edit the product,
    # any other user trying to access the edit form will be shown a 404 error
    if request.user != instance.user:
        raise Http404

    form = ProductForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        try:
            form.save()
            messages.success(request, 'Product updated')
            return HttpResponseRedirect(reverse('listings'))
        except ValueError:
            pass

    return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))

def single(request, slug):
    product = Product.objects.get(slug=slug)
    images = product.productimage_set.all()
    categories = product.category_set.all()
    comment_form = CommentForm(request.POST)
    comments = Comment.objects.filter(product=product)

    if request.user.is_authenticated():
        downloadable = request.user.has_purchased(product)

    edit = True

    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

def search_products(request):
    query = request.GET['query']
    products = Product.objects.filter(Q(description__icontains=query) | Q(title__icontains=query) | Q(headline__icontains=query) | Q(author__icontains=query) | Q(isbn_number__icontains=query), active=True)
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

def comment(request, slug):
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        try:
            comment = CommentForm(request.POST, instance=Comment(product=product, user=request.user))
            comment.save()
        except ValueError: # handle validation errors
            return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect(reverse('single_product', args=[product.slug]))

def manage_coupons(request, slug):
    product = Product.objects.get(slug=slug)

    if request.user != product.user:
        raise Http404

    # Products are fill-in at this stage instead just before save(), so that
    # we can have a validation depending on it (see CouponForm#clean_discount).
    params = fill_in_product_id(request.POST, product.pk)

    queryset = Coupon.objects.filter(product=product)
    CouponFormset = modelformset_factory(Coupon, form=CouponForm, can_delete=True)
    formset = CouponFormset(params or None, queryset=queryset)

    if request.method == 'POST' and formset.is_valid():
        try:
            coupons = formset.save(commit=False)
            for coupon in coupons:
                # Make sure the user is creating a coupon for her own product.
                if coupon.product.user != request.user:
                    return HttpResponseForbidden()
                coupon.save()
            return HttpResponseRedirect(reverse('manage_coupons', args=[product.slug]))
        except ValueError: # handle validation errors
            pass

    return render_to_response("products/manage_coupons.html", locals(), context_instance=RequestContext(request))

def fill_in_product_id(params, product_id):
    params = params.copy()

    for i in range(int(params.get('form-MAX_NUM_FORMS', 0))):
        if params.get('form-%s-discount' % i):
            params['form-%s-product' % i] = product_id
        else:
            break

    return params
