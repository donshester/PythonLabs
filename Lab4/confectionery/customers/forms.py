import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    date_of_birth = forms.DateField(label='Birth date', widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=20, label='Phone')
    first_name = forms.CharField(max_length=100, label='First Name')
    second_name = forms.CharField(max_length=100, label='Second Name')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'phone', 'first_name', 'second_name')

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - (
                        (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to register.")
        return date_of_birth

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^\+375\d{9}$', phone):
                raise forms.ValidationError("Phone number must be in the format +375XXXXXXXXX.")
        return phone
