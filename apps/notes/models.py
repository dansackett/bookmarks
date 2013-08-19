from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class Note(models.Model):
    """Notes models"""
    title = models.CharField(max_length=100, verbose_name='Note Name')
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True, verbose_name='Note')
    user = models.ForeignKey(User)
    category = models.CharField(max_length=100, verbose_name='Category')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        """Print the title as the representation of a note"""
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the view link for a note"""
        return ('view-note', (), {'category': self.category, 'slug': self.slug})

    @permalink
    def get_edit_url(self):
        """Return the edit link for a note"""
        return ('edit-note', (), {'category': self.category, 'slug': self.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a note"""
        return ('delete-note', (), {'category': self.category, 'slug': self.slug})

    @permalink
    def get_category_url(self):
        """Return the category link for a note"""
        return ('view-category', (), {'category': self.category})
