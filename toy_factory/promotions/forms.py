from django import forms
from .models import PromoCode

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['text', 'discount_percent', 'state']