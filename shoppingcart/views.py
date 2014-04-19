from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect
from django.core.urlresolvers import reverse
from products.models import Product

from .models import Shoppingcart, ShoppingcartItem


def shoppingcart(request):
    try:
        shoppingcart_id = request.session['shoppingcart_id']
        shoppingcart = Shoppingcart.objects.get(id=shoppingcart_id)
        items = shoppingcart.shoppingcartitem_set.all()
        total_price = sum(item.product.price for item in items)
        total_discount = sum(item.discount or 0 for item in items)
        total_after_discount = total_price - total_discount
    except KeyError:
        pass

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
