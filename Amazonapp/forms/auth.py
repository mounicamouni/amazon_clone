from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    mobileno = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mobileno'}),
                                help_text = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))


    # class Meta:
    #     model = User
    #     fields = ('username', 'mobileno','email', 'password1', 'password2', )

    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'user name'})
    )
    password1 = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    email = forms.EmailField(
        max_length=30,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )

class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'user name'})
    )
    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
