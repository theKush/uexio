from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import password_change

from products.models import Product, UserPurchase
from .models import UserProfile
from .forms import UserForm, ReviewSellerForm, UserProfileForm
# render the profile page with the
def profile(request, username):
    current_user_profile_url = get_current_user_profile_url(request)
    profile_user = User.objects.get(username=username)
    if not profile_user:
        raise Http404
    can_review = request.user.can_review(profile_user)
    products = Product.listing().filter(user=profile_user)
    products_sold_count = Product.objects.filter(user=profile_user, purchase__isnull=False).count()
    return render_to_response("profiles/profile.html", locals(), context_instance=RequestContext(request))
# render the edit profile page
def edit_profile(request):
    current_user_profile_url = get_current_user_profile_url(request)
    form = UserForm(request.POST or None, instance=request.user)
    profile_user = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(request.POST or None, instance=profile_user)
    if request.method == 'POST':
        try:
            form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
        except ValueError: # handle validation errors
            pass
    return render_to_response("profiles/edit_profile.html", locals(), context_instance=RequestContext(request))
# allow ability to change passwords
def edit_password(request):
    return password_change(request, template_name="profiles/edit_password.html",
                           extra_context={'current_user_profile_url': get_current_user_profile_url(request),
                                          'request': request})

# This action is invoked automatically after a successful password change and
# is only needed to provide a nice flash message to the user.
def password_change_done(request):
    messages.success(request, 'Your password has been changed.')
    return HttpResponseRedirect(reverse('edit_password'))
# list the user's library with downloadable materials
def library(request):
    current_user_profile_url = get_current_user_profile_url(request)
    if request.user.is_authenticated():
        products = request.user.purchased_products()
        return render_to_response("profiles/library.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404
# current listings created by the user
def listings(request):
    current_user_profile_url = get_current_user_profile_url(request)
    _products = Product.objects.filter(user=request.user)
    active_products = _products.filter(status=Product.ACTIVE)
    inactive_products = _products.filter(status=Product.INACTIVE)
    return render_to_response("profiles/listings.html", locals(), context_instance=RequestContext(request))
# purchases made by the user
def mypurchases(request):
    current_user_profile_url = get_current_user_profile_url(request)
    purchases = UserPurchase.objects.filter(user=request.user)
    return render_to_response("profiles/mypurchases.html", locals(), context_instance=RequestContext(request))
# items sold by the user
def mysolditems(request):
    current_user_profile_url = get_current_user_profile_url(request)
    products = Product.objects.filter(user=request.user, purchase__isnull=False)
    return render_to_response("profiles/mysolditems.html", locals(), context_instance=RequestContext(request))
# allow ability to review sellers
def review_seller(request, username):
    current_user_profile_url = get_current_user_profile_url(request)
    profile_user = User.objects.get(username=username)
    form = ReviewSellerForm(request.POST or None)

    if not request.user.can_review(profile_user):
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
