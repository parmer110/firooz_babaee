from dataclasses import field, fields

from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from account.models import CustomUser

class LoginForm(forms.Form):
  username = forms.CharField(max_length=63)
  password = forms.CharField(max_length=63, widget=forms.PasswordInput)
class CustomUserCrerationForm(UserCreationForm):
    
     class Meta:
        model=CustomUser
        fields=UserCreationForm.Meta.fields+('AccessLevel', 'phone','address')
        #fields=('username','email','AccessLevel',)
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=UserCreationForm.Meta.fields
    