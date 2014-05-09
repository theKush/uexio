from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def bootstrap_label_tag(field, size=2):
    return field.label_tag(attrs={'class': 'col-lg-%s control-label' % size})

@register.simple_tag
def bootstrap_field_tag(field):
    return field.as_widget(attrs={'class': 'form-control'})

@register.simple_tag
def bootstrap_textarea_tag(field):
    return field.as_textarea(attrs={'class': 'form-control'})

@register.simple_tag
def bootstrap_form_group_class(field):
    if field.errors:
        return 'form-group has-error'
    else:
        return 'form-group'

@register.simple_tag
def bootstrap_alert_class(message):
    if message.tags == 'success':
        return 'alert alert-dismissable alert-success'
    elif message.tags == 'info':
        return 'alert alert-dismissable alert-info'
    elif message.tags == 'warning':
        return 'alert alert-dismissable alert-warning'
    return 'alert alert-dismissable alert-danger'

from shoppingcart.views import is_product_in_cart

@register.simple_tag(takes_context=True)
def add_to_cart_button(context, product, css_class="btn btn-primary btn-block"):
    if is_product_in_cart(context['request'], product):
        url = reverse('remove_from_cart', args=[product.id])
        text = 'Product already in cart'
        label = 'Remove from'
    else:
        url = reverse('add_to_cart', args=[product.id])
        text = ''
        label = 'Add to'
    return '''<small>%(text)s</small>
        <a class="%(css_class)s" href="%(url)s">
            %(label)s <i class="fa fa-shopping-cart"></i>
        </a>''' % {"text": text, "css_class": css_class, "url": url, "label": label}
