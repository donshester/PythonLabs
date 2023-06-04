from django import forms
from django.forms import modelformset_factory
from .models import Order, OrderItem
class OrderForm(forms.ModelForm):
    delivery_date = forms.DateField(
        label='Delivery Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Order
        fields = ['delivery_date']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['min'] = 1