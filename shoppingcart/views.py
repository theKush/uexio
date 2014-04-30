from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect
from django.core.urlresolvers import reverse
from products.models import Product, Coupon

from .models import Shoppingcart, ShoppingcartItem
from .forms import ApplyCouponForm

def shoppingcart(request):
    coupon_form = ApplyCouponForm()
    items = _get_shopping_cart_items(request)
    total_price = sum(item.product.price for item in items)
    total_discount = sum(item.discount or 0 for item in items)
    total_after_discount = total_price - total_discount

    return render_to_response('shoppingcart/view_shoppingcart.html', locals(), context_instance=RequestContext(request))

def update_cart(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        product = False

    shoppingcart = _get_or_create_shopping_cart(request)

    if product:
        new_item, created = ShoppingcartItem.objects.get_or_create(shoppingcart=shoppingcart, product=product)
        if created:
            new_item.Shoppingcart = shoppingcart
            new_item.save()
            messages.success(request, 'Item added to cart')
        else:
            new_item.delete()
            messages.warning(request, 'Item removed from cart')
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
