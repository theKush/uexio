from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            autologin(form, request)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})

def autologin(form, request):
    "Automatically login user after registration"
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    login(request, user)
