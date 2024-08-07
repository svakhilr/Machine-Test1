from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))

    def authenticate_user(self):
        print(self.cleaned_data)
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        print(user.is_staff)
        return user