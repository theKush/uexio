from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def paypal_button(product):
    # TODO needs to securely register the transaction somehow by contacting paypal,
    # but if we're not the sellers then that's not possible
    # whatever we put into "return" will be spoofable
    return_url = request.build_absolute_uri(reverse('thankyou'))
    return PAYPAL_BUTTON_TEMPLATE % (product.user.email, product.title, product.price, return_url)

PAYPAL_BUTTON_TEMPLATE = """
<form name="_xclick" action="https://www.paypal.com/cgi-bin/webscr" method="post" style="display: inline;">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="%s">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="item_name" value="%s">
<input type="hidden" name="amount" value="%.02f">
<input type="hidden" name="return" value="%s">
<button type="submit" class="btn btn-primary">Add to <i class="fa fa-shopping-cart"></i></button>
</form>
"""
