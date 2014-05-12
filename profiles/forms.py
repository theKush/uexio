from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import SellerReview, UserProfile
# creating a userform for editing user information
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
# creating user form for addition fields
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('paypal', 'phonenumber')
# form to review sellers
class ReviewSellerForm(ModelForm):
    class Meta:
        model = SellerReview
        fields = ('rating', 'content')

