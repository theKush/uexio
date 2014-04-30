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

@register.simple_tag
def add_to_cart_button(product, css_class="btn btn-primary"):
    url = reverse('update_cart', args=[product.id])
    return '<a class="%s" href="%s">Add to <i class="fa fa-shopping-cart"></i></a>' % (css_class, url)
