from django import template
from django.core.urlresolvers import reverse

from uexio.settings import PAYPAL_EMAIL, PAYPAL_HOST

register = template.Library()

@register.simple_tag
def paypal_button(request, cart):
    return_url = request.build_absolute_uri(reverse('thankyou'))
    notify_url = request.build_absolute_uri(reverse('paypal_notification', args=[cart.id]))
    return PAYPAL_BUTTON_TEMPLATE % {
        'host': PAYPAL_HOST,
        'email': PAYPAL_EMAIL,
        'title': cart.transaction_name(),
        'total': cart.total_after_discount(),
        'notify_url': notify_url,
        'return_url': return_url}

# https://developer.paypal.com/docs/classic/paypal-payments-standard/integration-guide/formbasics/
PAYPAL_BUTTON_TEMPLATE = """
<form name="_xclick" action="https://%(host)s/cgi-bin/webscr" method="post" class="pull-right">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="%(email)s">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="item_name" value="%(title)s">
<input type="hidden" name="amount" value="%(total).02f">
<input type="hidden" name="notify_url" value="%(notify_url)s">
<input type="hidden" name="return" value="%(return_url)s">
<button type="submit" class="btn btn-primary btn-lg">Pay with PayPal</button>
</form>
"""
