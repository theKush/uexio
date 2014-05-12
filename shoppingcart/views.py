import logging

from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from products.models import Product, Coupon

from .models import Shoppingcart, ShoppingcartItem
from .forms import ApplyCouponForm
from .paypal_integration import transaction_data_matches, queue_paypal_notification
# render the shopping cart along the coupon form
def shoppingcart(request):
    coupon_form = ApplyCouponForm()
    shoppingcart = _get_shopping_cart(request)

    return render_to_response('shoppingcart/view_shoppingcart.html', locals(), context_instance=RequestContext(request))
# allow ability to add items to cart and display alert messages
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    shoppingcart = _get_or_create_shopping_cart(request)

    _, created = ShoppingcartItem.objects.get_or_create(shoppingcart=shoppingcart, product=product)
    if created:
        messages.success(request, 'Item added to cart')
    else:
        messages.warning(request, 'Item already in cart')

    return HttpResponseRedirect(reverse('shoppingcart'))
# allow ability to remove from cart and display alert messages
def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    shoppingcart = _get_or_create_shopping_cart(request)

    try:
        item = ShoppingcartItem.objects.get(shoppingcart=shoppingcart, product=product)
        item.delete()
        messages.warning(request, 'Item removed from cart')
    except ShoppingcartItem.DoesNotExist:
        messages.warning(request, 'Item not in cart')

    return HttpResponseRedirect(reverse('shoppingcart'))
# allow ability to apply coupon codes in cart and display alert messages
def apply_coupon(request):
    form = ApplyCouponForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                applied = False
                code = form.cleaned_data['code']
                coupon = Coupon.objects.get(code=code)
                items = _get_shopping_cart_items(request)
                for item in items:
                    if item.product == coupon.product:
                        item.discount = coupon.discount
                        item.save()
                        messages.success(request, 'Code applied')
                        applied = True
                if not applied:
                    messages.warning(request, "Coupon code doesn't apply to any of those products")
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon code invalid')
    return HttpResponseRedirect(reverse('shoppingcart'))
# after a successful transaction display a thank you page.
@csrf_exempt
def thankyou(request):
    _clear_shopping_cart(request)
    return render_to_response('shoppingcart/thankyou.html', locals(), context_instance=RequestContext(request))

# create paypal notifications with shoppingcart ids
@csrf_exempt
def paypal_notification(request, id):
    shoppingcart = get_object_or_404(Shoppingcart, id=id)
    params = _flatten_params(request.POST)
    if transaction_data_matches(shoppingcart, params):
        queue_paypal_notification(shoppingcart, params)
        return HttpResponse('')
    else:
        logger = logging.getLogger('debug')
        logger.error('IPN failed for cart id=%s, params=%s' % (id, params))
        return HttpResponseBadRequest('')

def _flatten_params(params):
    return dict([k, v[0]] for k, v in dict(params).iteritems())

# get the total number of items in shopping cart
def _get_shopping_cart_items(request):
    shoppingcart = _get_shopping_cart(request)
    if shoppingcart:
        return shoppingcart.shoppingcartitem_set.all()
    else:
        return []
# shopping cart helper function that creates shopping cart with shopping cart id and the user
def _get_shopping_cart(request):
    try:
        shoppingcart_id = request.session['shoppingcart_id']
        shoppingcart = Shoppingcart.objects.get(id=shoppingcart_id, user=request.user)
        return shoppingcart
    except (KeyError, Shoppingcart.DoesNotExist):
        return None
# get or create a new shopping cart for the user session
def _get_or_create_shopping_cart(request):
    shoppingcart = _get_shopping_cart(request)
    if not shoppingcart:
        shoppingcart = Shoppingcart(user=request.user)
        shoppingcart.save()
        request.session['shoppingcart_id'] = shoppingcart.id
    return shoppingcart
# clear the shopping cart session
def _clear_shopping_cart(request):
    del request.session['shoppingcart_id']
# check if product is already in the cart
def is_product_in_cart(request, product):
    items = _get_shopping_cart_items(request)
    for item in items:
        if item.product == product:
            return True
    return False
