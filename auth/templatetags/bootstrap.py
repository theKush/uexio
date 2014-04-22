from django import template

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
