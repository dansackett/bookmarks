import datetime
import re

from django import forms
from django.contrib.auth.models import User

from auth.utils import password_is_good, valid_username


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'Username is required.'})
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': 'Password is required.'})


class RegistrationForm(forms.Form):
    help_text = {
        'username': 'Can only contain letters, numbers and \'@/./+/-/_\' \
                     characters.',
        'password': 'Passwords must be at least 8 characters in length.'
    }

    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text=help_text['password'])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not valid_username(username):
            raise forms.ValidationError(self.help_text['username'])

        if User.objects.filter(username=username):
            raise forms.ValidationError('That username already exists.')

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        is_good, message = password_is_good(password)

        if not is_good:
            raise forms.ValidationError(message)

        return password

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password is not None and confirm_password is not None:
            if password != confirm_password:
                raise forms.ValidationError('Your passwords don\'t match.')

        return cleaned_data

    def save(self):
        user = User(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            is_active=True,
            is_staff=False,
            date_joined=datetime.datetime.now(),
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user
