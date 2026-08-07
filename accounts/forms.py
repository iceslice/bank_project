from django import forms
from django.contrib.auth.models import User
from .models import Transaction

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
