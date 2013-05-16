from datetime import datetime

from django import forms
from django.template.defaultfilters import slugify

from reminders.models import Reminder


class BaseReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        exclude = ('slug', 'user', 'dismissed', 'sent',)


class NewReminderForm(BaseReminderForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.date = kwargs.pop('date', datetime.now().date())
        super(NewReminderForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = self.date

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Reminder.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a reminder with that title.')

        return title

    def save(self, commit=True):
        reminder = super(NewReminderForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        reminder.slug = slugify(title)
        reminder.user = self.user
        reminder.save()
        return reminder


class EditReminderForm(BaseReminderForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditReminderForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.instance.title != title:
            if Reminder.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a reminder with that title.')

        return title

    def save(self, commit=True):
        reminder = super(EditReminderForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        date = self.cleaned_data.get('date')
        reminder.slug = slugify(title)
        reminder.user = self.user
        reminder.save()
        return reminder
