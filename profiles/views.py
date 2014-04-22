from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profiles.models import Product
from .models import UserPurchase
from .forms import EditProfileForm, ReviewSellerForm

def profile(request, username):
    current_user_profile_url = get_current_user_profile_url(request)
    profile_user = User.objects.get(username=username)
    products = Product.objects.filter(user=request.user, active=True)
    if not profile_user:
        raise Http404
    return render_to_response("profiles/profile.html", locals(), context_instance=RequestContext(request))

def edit_profile(request):
    current_user_profile_url = get_current_user_profile_url(request)
    form = EditProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        try:
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
        except ValueError: # handle validation errors
            pass
    return render_to_response("profiles/edit_profile.html", locals(), context_instance=RequestContext(request))

def library(request):
    current_user_profile_url = get_current_user_profile_url(request)
    if request.user.is_authenticated():
        products = request.user.purchased_products()
        return render_to_response("profiles/library.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

def listings(request):
    current_user_profile_url = get_current_user_profile_url(request)
    products = Product.objects.filter(user=request.user)
    return render_to_response("profiles/listings.html", locals(), context_instance=RequestContext(request))

def review_seller(request, username):
    current_user_profile_url = get_current_user_profile_url(request)
    profile_user = User.objects.get(username=username)
    form = ReviewSellerForm(request.POST)

    if profile_user == request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        try:
            review = form.save(commit=False)
            review.seller = profile_user
            review.author = request.user
            review.save()
            return HttpResponseRedirect(reverse('profile', args=[profile_user.username]))
        except ValueError: # handle validation errors
            pass
    return render_to_response("profiles/review_seller.html", locals(), context_instance=RequestContext(request))

def get_current_user_profile_url(request):
    return reverse('profile', args=[request.user.username])
