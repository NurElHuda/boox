
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', max_length=100, widget=forms.TextInput(attrs={"class":"form-control px-2", "id":"floatingPassword", "placeholder":"Password"}))
