from django import template
import hashlib

register = template.Library()

@register.simple_tag
def gravatar_image_url(user, size=80):
    md5 = hashlib.md5()
    md5.update(user.email.strip().lower())
    hash = md5.hexdigest()
    return "http://www.gravatar.com/avatar/%s?s=%s&d=mm" % (hash, size)
