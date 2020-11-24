from django import forms
from .models import *

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseConfirmForm(forms.Form):    
    deliverDate = forms.DateTimeField(input_formats=['%d/%m/%Y %I:%M %p'])
