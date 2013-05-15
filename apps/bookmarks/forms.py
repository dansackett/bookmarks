from django import forms
from django.template.defaultfilters import slugify

from bookmarks.models import Bookmark
from tags.models import Tag


class BaseBookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        exclude = ('slug', 'user')


class NewBookmarkForm(BaseBookmarkForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewBookmarkForm, self).__init__(*args, **kwargs)

        self.tags_error = {'required': 'You have to choose a tag first!'}
        self.fields['tag'].error_messages = self.tags_error
        tags = Tag.objects.filter(user=self.user)
        self.fields['tag'].choices = [(tag.pk, tag.title) for tag in tags]
        self.fields['url'].label = 'URL'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Bookmark.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a bookmark with that title.')

        return title

    def save(self, commit=True):
        bookmark = super(NewBookmarkForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        bookmark.slug = slugify(title)
        bookmark.user = self.user
        bookmark.save()
        return bookmark


class EditBookmarkForm(BaseBookmarkForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.bookmark = kwargs.pop('bookmark', None)
        super(EditBookmarkForm, self).__init__(*args, **kwargs)
        tags = Tag.objects.filter(user=self.user)
        self.fields['tag'].choices = [(tag.pk, tag.title) for tag in tags]

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.instance.title != title:
            if Bookmark.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a bookmark with that title.')

        return title

    def save(self, commit=True):
        bookmark = super(EditBookmarkForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        bookmark.slug = slugify(title)
        bookmark.user = self.user
        bookmark.save()
        return bookmark
