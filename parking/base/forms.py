from django.forms import ModelForm
from django import forms
from .models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = searchData
        fields = ('address',)
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
