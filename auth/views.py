from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from profiles.forms import UserProfileForm
from .forms import UserCreateForm
# allow user to register
def register(request):
    # If it's a HTTP POST, we're interest in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information
        # Note that we make use of both UserCreationForm and UserProfileForm.
        user_form = UserCreateForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # AutoLogin the user after registration
            autologin(user_form, request)

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance
            profile.save()

            # Redirect the user to home
            return HttpResponseRedirect("/")
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal
        # They'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances
    # These forms will be blank, ready for user input
    else:
        user_form = UserCreateForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context
    return render(request, "registration/register.html", {'user_form': user_form, 'profile_form': profile_form})

def autologin(form, request):
    "Automatically login user after registration"
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    login(request, user)
