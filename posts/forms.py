from django.contrib.auth.models import User
from django import forms
#from .models import Profile
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    city = forms.CharField(max_length=100)
    phone=forms.IntegerField()
    class Meta:
        model=User
        fields=['username','password']

class LoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','password']