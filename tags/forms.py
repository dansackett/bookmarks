import datetime

from django import forms
from django.template.defaultfilters import slugify

from tags.models import Tag


class NewTagForm(forms.Form):
    title = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewTagForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Tag.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a tag with that title.')

        return title

    def save(self):
        title = self.cleaned_data.get('title')
        tag = Tag(
            title=title,
            slug=slugify(title),
            user=self.user,
        )
        tag.save()


class EditTagForm(forms.Form):
    title = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.tag = kwargs.pop('tag', None)
        kwargs['initial'] = self._build_initial()
        super(EditTagForm, self).__init__(*args, **kwargs)

    def _build_initial(self):
        user = self.user
        initial = {
            'title': self.tag.title,
        }

        return initial

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.tag.title != title:
            if Tag.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a tag with that title.')

        return title

    def save(self):
        title = self.cleaned_data.get('title')
        tag = self.tag
        tag.title = title
        tag.modified_on = datetime.datetime.now()
        tag.save()
