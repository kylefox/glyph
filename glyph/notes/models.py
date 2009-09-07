from datetime import datetime
from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import striptags, truncatewords, timesince
from tagging.fields import TagField

class Note(models.Model):
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=50)
    tags = TagField(blank=True)
    publish_date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        get_latest_by = 'publish_date'
        ordering = ('-publish_date',)
        unique_together = (('publish_date', 'slug'),)
    
    def __unicode__(self):
        return self.title or truncatewords(self.body, 15)
        
    def permalink(self, text=None):
        if text is None:
            text = self.title
        return mark_safe('<a class="permalink" href="%s" rel="bookmark permalink" title="Permalink to this note">%s</a>' % (self.get_absolute_url(), text))
        
    def permalink_timesince(self):
        return self.permalink(timesince(self.publish_date) + " ago")
        
    @models.permalink
    def get_absolute_url(self):
        return ('notes.note_detail', (), {
            'year': self.publish_date.strftime('%Y'),
            'month': self.publish_date.strftime('%b').lower(),
            'day': self.publish_date.strftime('%d'),
            'slug': self.slug
        })

    def approved_comments(self):
        from comments.models import Comment
        return Comment.objects.approved_for_object(self)