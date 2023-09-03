from datetime import date, timedelta

from django import forms
from django.forms import modelformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    delivery_date = forms.DateField(
        label='Delivery Date',
        widget=forms.DateInput(attrs={'type': 'date'} )
    )

    class Meta:
        model = Order
        fields = ['delivery_date']

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if delivery_date:
            today = date.today()
            if delivery_date <= today:
                raise forms.ValidationError("Delivery date must be in the future.")
            max_delivery_date = today + timedelta(days=365)
            if delivery_date > max_delivery_date:
                raise forms.ValidationError("Delivery date must be within 365 days from today.")
        return delivery_date


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['min'] = 1

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        if product and quantity:
            if quantity > product.quantity:
                raise forms.ValidationError("The entered quantity exceeds the available quantity.")
        return quantity
