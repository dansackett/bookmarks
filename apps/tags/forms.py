from django import forms
from django.template.defaultfilters import slugify

from tags.models import Tag


class BaseTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        exclude = ('slug', 'user')


class NewTagForm(BaseTagForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewTagForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Tag.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a tag with that title.')

        return title

    def save(self, commit=True):
        tag = super(NewTagForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        tag.slug = slugify(title)
        tag.user = self.user
        tag.save()
        return tag


class EditTagForm(BaseTagForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditTagForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.instance.title != title:
            if Tag.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a tag with that title.')

        return title

    def save(self, commit=True):
        tag = super(EditTagForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        tag = self.instance
        tag.slug = slugify(title)
        tag.save()
        return tag
