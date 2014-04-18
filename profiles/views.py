from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse

from .models import UserPurchase
from .forms import EditProfileForm

def profile(request):
    return render_to_response("profiles/profile.html", locals(), context_instance=RequestContext(request))

def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        try:
            form.save()
            return HttpResponseRedirect(reverse('profile'))
        except ValueError: # handle validation errors
            pass
    return render_to_response("profiles/edit_profile.html", locals(), context_instance=RequestContext(request))

def library(request):
    if request.user.is_authenticated():
        products = request.user.purchased_products()
        return render_to_response("profiles/library.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404
