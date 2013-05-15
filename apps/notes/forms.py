from django import forms
from django.template.defaultfilters import slugify

from notes.models import Note


class BaseNoteForm(forms.ModelForm):

    category_choices = [('no_category', 'No Category'), ('bar', 'Bar'),
                        ('book', 'Book'), ('food', 'Food'), ('idea', 'Idea'),
                        ('movie', 'Movie'), ('music', 'Music'),
                        ('person', 'Person'), ('place', 'Place')]

    category = forms.ChoiceField(choices=category_choices, widget=forms.Select)

    class Meta:
        model = Note
        exclude = ('slug', 'user', 'category')


class NewNoteForm(BaseNoteForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewNoteForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Note.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a note with that title.')

        return title

    def save(self, commit=True):
        note = super(NewNoteForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        note.slug = slugify(title)
        note.user = self.user
        note.category = self.cleaned_data.get('category')
        note.save()
        return note


class EditNoteForm(BaseNoteForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditNoteForm, self).__init__(*args, **kwargs)
        self.fields['category'].initial = self.instance.category


    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.instance.title != title:
            if Note.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a note with that title.')

        return title

    def save(self, commit=True):
        note = super(EditNoteForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        note = self.instance
        note.slug = slugify(title)
        note.category = self.cleaned_data.get('category')
        note.save()
        return note
