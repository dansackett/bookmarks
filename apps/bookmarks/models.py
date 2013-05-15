from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from tags.models import Tag


class Bookmark(models.Model):
    """Bookmarks models"""
    title = models.CharField(max_length=100, verbose_name="Bookmark Name")
    slug = models.SlugField()
    user = models.ForeignKey(User)
    description = models.TextField(blank=True, null=True, verbose_name="Notes")
    tag = models.ForeignKey(Tag, verbose_name="Tagged As")
    url = models.URLField(verbose_name="Bookmark URL")
    favorited = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        """Print the title as the representation of a bookmark"""
        return self.title

    @permalink
    def get_edit_url(self):
        """Return the edit link for a bookmark"""
        return ('edit-bookmark', (), {'slug': self.slug,
                                      'tag_slug': self.tag.slug})

    @permalink
    def get_favorite_url(self):
        """Return the favorite link for a bookmark"""
        return ('favorite-bookmark', (), {'slug': self.slug,
                                          'tag_slug': self.tag.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a bookmark"""
        return ('delete-bookmark', (), {'slug': self.slug,
                                        'tag_slug': self.tag.slug})
