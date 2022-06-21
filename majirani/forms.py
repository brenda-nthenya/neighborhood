from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email=forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','password1','password2']

class NewBusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['Admin', 'pub_date', 'admin_profile']

class NewNeighborhoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        exclude = ['Admin', 'pub_date', 'admin_profile']