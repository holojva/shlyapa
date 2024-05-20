from django import forms

class LoginForm(forms.Form) :
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
class RegisterForm(forms.Form) :
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
class WordForm(forms.Form) :
    word = forms.CharField(max_length=30)
class RoomForm(forms.Form) :
    name = forms.CharField(max_length=30)
    time = forms.CharField(max_length=5)