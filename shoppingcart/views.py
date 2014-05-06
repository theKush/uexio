from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect
from django.core.urlresolvers import reverse
from products.models import Product, Coupon

from .models import Shoppingcart, ShoppingcartItem
from .forms import ApplyCouponForm

def shoppingcart(request):
    coupon_form = ApplyCouponForm()
    shoppingcart = _get_shopping_cart(request)

    return render_to_response('shoppingcart/view_shoppingcart.html', locals(), context_instance=RequestContext(request))

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    shoppingcart = _get_or_create_shopping_cart(request)

    _, created = ShoppingcartItem.objects.get_or_create(shoppingcart=shoppingcart, product=product)
    if created:
        messages.success(request, 'Item added to cart')
    else:
        messages.warning(request, 'Item already in cart')

    return HttpResponseRedirect(reverse('shoppingcart'))

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

def _get_shopping_cart_items(request):
    shoppingcart = _get_shopping_cart(request)
    if shoppingcart:
        return shoppingcart.shoppingcartitem_set.all()
    else:
        return []

def _get_shopping_cart(request):
    try:
        shoppingcart_id = request.session['shoppingcart_id']
        shoppingcart = Shoppingcart.objects.get(id=shoppingcart_id)
        return shoppingcart
    except (KeyError, Shoppingcart.DoesNotExist):
        return None

def _get_or_create_shopping_cart(request):
    shoppingcart = _get_shopping_cart(request)
    if not shoppingcart:
        shoppingcart = Shoppingcart()
        shoppingcart.save()
        request.session['shoppingcart_id'] = shoppingcart.id
    return shoppingcart

def is_product_in_cart(request, product):
    items = _get_shopping_cart_items(request)
    for item in items:
        if item.product == product:
            return True
    return False
