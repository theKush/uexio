from django.contrib import messages
from django.shortcuts import render_to_response, Http404, RequestContext, HttpResponseRedirect

from products.models import Product
from products.views import check_product

from .models import Shoppingcart, ShoppingcartItem


def shoppingcart(request):

    return render_to_response('shoppingcart/view_shoppingcart.html', locals(), context_instance=RequestContext(request))


def add_to_cart(request, id):
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
            messages.success(request, 'cart item added')
        return HttpResponseRedirect('/cart/')

