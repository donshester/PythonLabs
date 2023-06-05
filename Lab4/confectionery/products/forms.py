from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0)
    quantity = forms.IntegerField(min_value=0)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not any(char.isalpha() for char in name):
            raise forms.ValidationError("Name must contain at least one letter.")
        return name
    class Meta:
        model = Product
        fields = ['name', 'price', 'unit', 'manufacturer', 'category', 'quantity']
