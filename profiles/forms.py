from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import SellerReview, UserProfile

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('paypal', 'phonenumber')

class ReviewSellerForm(ModelForm):
    class Meta:
        model = SellerReview
        fields = ('rating', 'content')

