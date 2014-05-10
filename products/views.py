import os

from mimetypes import guess_type

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Product, Category, ProductImage, Comment, Coupon
from .forms import ProductForm, ProductImageForm, CommentForm, CouponForm, ProductImageFormSet
from .helpers import product_url

def list_all(request):
    title = "All Products"
    products = Product.listing()
    return _all_products_page(request, locals())

def search_products(request):
    query = request.GET['query']
    products = Product.listing().filter(Q(description__icontains=query) | Q(title__icontains=query) | Q(headline__icontains=query) | Q(author__icontains=query) | Q(isbn_number__icontains=query))
    title = "Products matching \"" + query + "\""
    return _all_products_page(request, locals())

def category(request, slug):
    category = Category.objects.get(slug=slug)
    title = "Products in \"" + category.title + "\""
    products = Product.listing().filter(category=category)
    return _all_products_page(request, locals())

def _all_products_page(request, context):
    categories = Category.objects.all()
    order = _order(request)
    page = _paginate(context['products'].order_by(order), request)
    context.update(locals())
    return render_to_response("products/all.html",
                              context,
                              context_instance=RequestContext(request))

def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    image_form = ProductImageForm(request.POST or None, request.FILES or None)

    if form.is_valid() and image_form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.slug = slugify(form.cleaned_data['title'])
        product.save()
        image = image_form.save(commit=False)
        image.product = product
        image.featured_image = True
        image.save()
        return HttpResponseRedirect(product_url(product))

    return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))

def manage_product_image(request, id):
    product = Product.objects.get(id=id)

    if request.user != product.user:
        raise Http404

    # this queries the images and ensures that the correct image is selected
    queryset = ProductImage.objects.filter(product__id=id)
    formset = ProductImageFormSet(request.POST or None, request.FILES or None, queryset=queryset)

    if request.method == 'POST' and formset.is_valid():
        images = formset.save(commit=False)
        for image in images:
            image.product = product
            image.save()
        return HttpResponseRedirect(reverse('manage_product_image', args=[product.id]))

    return render_to_response("products/manage_images.html", locals(), context_instance=RequestContext(request))

def edit_product(request, id):
    instance = Product.objects.get(id=id)
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

def single(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    images = product.productimage_set.all()
    comment_form = CommentForm(request.POST)
    comments = Comment.objects.filter(product=product)

    if request.user.is_authenticated():
        downloadable = request.user.has_purchased(product)

    edit = True

    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

def activate_product(request, id):
    product = Product.objects.get(id=id)
    product.status = Product.ACTIVE
    product.save()
    return HttpResponseRedirect(reverse('listings'))

def deactivate_product(request, id):
    product = Product.objects.get(id=id)
    product.status = Product.INACTIVE
    product.save()
    return HttpResponseRedirect(reverse('listings'))

def comment(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        try:
            comment = CommentForm(request.POST, instance=Comment(product=product, user=request.user))
            comment.save()
        except ValueError: # handle validation errors
            return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect(product_url(product))

def manage_coupons(request, id):
    product = Product.objects.get(id=id)

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
            return HttpResponseRedirect(reverse('manage_coupons', args=[product.id]))
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

def _order(request):
    order = request.GET.get('order')
    if order in ['price', '-price']:
        return order
    return 'price' # the default sorting order

def _paginate(products, request):
    paginator = Paginator(products, 15)

    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.page(paginator.num_pages)
