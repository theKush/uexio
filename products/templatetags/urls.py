from django import template

from ..helpers import product_url

register = template.Library()
register.simple_tag(product_url)
