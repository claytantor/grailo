from django import forms

__author__ = 'claygraham'

class LoginForm(forms.Form):
    public_key = forms.CharField(max_length=250)
    password = forms.CharField(max_length=250,widget=forms.HiddenInput())

class RegisterForm(forms.Form):
    handel = forms.CharField(max_length=32,widget=forms.HiddenInput())
    public_key = forms.CharField(max_length=250,widget=forms.HiddenInput())
    pw_encrypted = forms.CharField(max_length=512,widget=forms.HiddenInput())
    pw_unencrypted = forms.CharField(max_length=128,widget=forms.HiddenInput())
    avatar_img = forms.CharField(max_length=16000,widget=forms.HiddenInput());
