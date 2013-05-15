from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class Reminder(models.Model):
    """Reminders models"""
    title = models.CharField(max_length=100, verbose_name="Reminder Name")
    slug = models.SlugField()
    user = models.ForeignKey(User)
    description = models.TextField(blank=True, null=True, verbose_name="Notes")
    date = models.DateTimeField(verbose_name="Remind Date")
    dismissed = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        """Print the title as the representation of a reminder"""
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the absolute link for a reminder"""
        return ('view-reminder', (), {'slug': self.slug})

    @permalink
    def get_edit_url(self):
        """Return the edit link for a reminder"""
        return ('edit-reminder', (), {'slug': self.slug})

    @permalink
    def get_dismiss_url(self):
        """Return the favorite link for a reminder"""
        return ('dismiss-reminder', (), {'slug': self.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a reminder"""
        return ('delete-reminder', (), {'slug': self.slug})
