import datetime
import re

from django import forms
from django.core import validators
from django.contrib.auth.models import User

from auth.utils import password_is_good, valid_username


class ProfileForm(forms.Form):
    username_help_text = 'Usernames can be 30 characters or fewer contaning \
                          letters, numbers and \'@/./+/-/_\' characters.'

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        kwargs['initial'] = self._build_initial()
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def _build_initial(self):
        user = self.user
        initial = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }

        return initial

    def clean_password(self):
        password = self.cleaned_data.get('password')
        is_good, message = password_is_good(password)

        if password:
            if not is_good:
                raise forms.ValidationError(message)

        return password

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password is not None and confirm_password is not None:
            if password != confirm_password:
                raise forms.ValidationError('Your passwords don\'t match.')

        return cleaned_data

    def save(self):
        user = self.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data.get('password'))
        user.save()
