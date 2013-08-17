from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tags models"""
    title = models.CharField(max_length=100, verbose_name='Tag Name')
    slug = models.SlugField()
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        """Print the title as the representation of a tag"""
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the view link for a tag"""
        return ('view-tag', (), {'slug': self.slug})

    @permalink
    def get_edit_url(self):
        """Return the edit link for a tag"""
        return ('edit-tag', (), {'slug': self.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a tag"""
        return ('delete-tag', (), {'slug': self.slug})

    def bookmarks_count(self, tag=None):
        # late binding to avoid ciclical import
        from bookmarks.models import Bookmark
        if tag:
            return Bookmark.objects.filter(tag=tag).count()
        else:
            return Bookmark.objects.filter(tag=self).count()
