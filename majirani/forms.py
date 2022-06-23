from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email=forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  
    class Meta:
        model = User
        fields=['username','email','password1','password2']

class NewBusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name','description','email']

class NewNeighborhoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ['name','description', 'location',
         'police_number', 'health_number',
          'occupants_count']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title','post','hood']

class UserUpdateForm(forms.ModelForm):
      email = forms.EmailField()
      class Meta:
        model = User
        fields = ['username','email'] 

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')