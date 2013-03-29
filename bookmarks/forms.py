import datetime

from django import forms
from django.template.defaultfilters import slugify

from bookmarks.models import Bookmark
from tags.models import Tag


class NewBookmarkForm(forms.Form):
    tags_error = {'required': 'You need to have a tag to add a bookmark'}

    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)
    url = forms.URLField()
    tag = forms.ChoiceField(widget=forms.Select, error_messages=tags_error)
    favorited = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewBookmarkForm, self).__init__(*args, **kwargs)

        tags = Tag.objects.filter(user=self.user)
        self.fields['tag'].choices = [(tag.pk, tag.title) for tag in tags]


    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Bookmark.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a bookmark with that title.')

        return title

    def save(self):
        title = self.cleaned_data.get('title')
        tag = Tag.objects.get(pk=self.cleaned_data.get('tag'))
        bookmark = Bookmark(
            title=title,
            slug=slugify(title),
            user=self.user,
            tag=tag,
            description=self.cleaned_data.get('description'),
            url=self.cleaned_data.get('url'),
            favorited=self.cleaned_data.get('favorited')
        )
        bookmark.save()


class EditBookmarkForm(forms.Form):

    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)
    url = forms.URLField()
    tag = forms.ChoiceField(widget=forms.Select)
    favorited = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.bookmark = kwargs.pop('bookmark', None)
        kwargs['initial'] = self._build_initial()
        super(EditBookmarkForm, self).__init__(*args, **kwargs)

        tags = Tag.objects.filter(user=self.user)
        self.fields['tag'].choices = [(tag.pk, tag.title) for tag in tags]

    def _build_initial(self):
        user = self.user
        initial = {
            'title': self.bookmark.title,
            'description': self.bookmark.description,
            'url': self.bookmark.url,
            'favorited': self.bookmark.favorited,
            'tag': self.bookmark.tag.pk,
        }

        return initial

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.bookmark.title != title:
            if Bookmark.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a bookmark with that title.')

        return title

    def save(self):
        tag = Tag.objects.get(pk=self.cleaned_data.get('tag'))
        bookmark = self.bookmark
        bookmark.title = self.cleaned_data.get('title')
        bookmark.slug = slugify(self.cleaned_data.get('title'))
        bookmark.user = self.user
        bookmark.tag = tag
        bookmark.description = self.cleaned_data.get('description')
        bookmark.url = self.cleaned_data.get('url')
        bookmark.favorited = self.cleaned_data.get('favorited')
        bookmark.modified_on = datetime.datetime.now()
        bookmark.save()
