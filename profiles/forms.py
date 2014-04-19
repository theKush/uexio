from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import SellerReview

class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ReviewSellerForm(ModelForm):
    class Meta:
        model = SellerReview
        fields = ('content',)
