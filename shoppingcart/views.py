from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect
from django.core.urlresolvers import reverse
from products.models import Product, Coupon

from .models import Shoppingcart, ShoppingcartItem
from .forms import ApplyCouponForm

def shoppingcart(request):
    coupon_form = ApplyCouponForm()
    items = _get_shooping_cart_items(request)
    total_price = sum(item.product.price for item in items)
    total_discount = sum(item.discount or 0 for item in items)
    total_after_discount = total_price - total_discount

    return render_to_response('shoppingcart/view_shoppingcart.html', locals(), context_instance=RequestContext(request))

def update_cart(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        product = False

    try:
        shoppingcart_id = request.session['shoppingcart_id']
    except:
        shoppingcart_id = False

    try:
        shoppingcart = Shoppingcart.objects.get(id=shoppingcart_id)
    except Shoppingcart.DoesNotExist:
        shoppingcart = Shoppingcart()
        shoppingcart.save()
        request.session['shoppingcart_id'] = shoppingcart.id

    if product:
        new_item, created = ShoppingcartItem.objects.get_or_create(shoppingcart=shoppingcart, product=product)
        if created:
            new_item.Shoppingcart = shoppingcart
            new_item.save()
            messages.success(request, 'cart item added')
        else:
            new_item.delete()
            messages.success(request, 'cart item remove')
        return HttpResponseRedirect(reverse('shoppingcart'))

def apply_coupon(request):
    form = ApplyCouponForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                code = form.cleaned_data['code']
                coupon = Coupon.objects.get(code=code)
                items = _get_shooping_cart_items(request)
                for item in items:
                    if item.product == coupon.product:
                        item.discount = coupon.discount
                        item.save()
            except Coupon.DoesNotExist:
                pass
    return HttpResponseRedirect(reverse('shoppingcart'))

def _get_shooping_cart_items(request):
    try:
        shoppingcart_id = request.session['shoppingcart_id']
        shoppingcart = Shoppingcart.objects.get(id=shoppingcart_id)
        return shoppingcart.shoppingcartitem_set.all()
    except KeyError:
        return []
