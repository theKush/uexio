from django import forms
# form to apply coupon codes in the shopping cart
class ApplyCouponForm(forms.Form):
    code = forms.CharField(max_length=20)

