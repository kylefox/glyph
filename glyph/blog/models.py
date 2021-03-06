from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatewords_html
from django.core.urlresolvers import reverse

from tagging.fields import TagField
from tagging.models import Tag

from glyph.utils.pinger import send_pings

class PostManager(models.Manager):
    
    def published(self):
        return self.get_query_set().filter(status=Post.PUBLISHED, publish_date__lte = datetime.now()).order_by('-publish_date')
        
    def draft(self):
        return self.get_query_set().filter(status=Post.DRAFT)

class Post(models.Model):
    
    objects = PostManager()
    
    PUBLISHED = 'published'
    DRAFT = 'draft'
    
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
    )
    
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(editable=False, default=datetime.now)
    modified_at = models.DateTimeField(editable=False)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    tags = TagField(blank=True)
    body = models.TextField(blank=True, help_text='Format with <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a>')
    publish_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    summary = models.TextField(blank=True)
    
    class Meta:
        unique_together = (('slug', 'publish_date'),)
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'
    
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        self.modified_at = datetime.now()
        if self.status == Post.PUBLISHED:
            send_pings(self, reverse("feeds.blog"))
        return super(Post, self).save(*args, **kwargs)
        
    def permalink(self, text=None, title=None):
        if text is None:
            text = self.title
        if title is None:
            title = "Permalink to this post"
        return mark_safe('<a href="%s" rel="bookmark permalink" title="%s">%s</a>' % (self.get_absolute_url(), title, text))
        
    def lead_in(self):
        html = truncatewords_html(self.content, 50)
        permalink = self.permalink(text="(more)", title="Read full article")
        return mark_safe("%s %s" % (html, permalink))
        
    def publish_date_ISO8601(self):
        # Trying to implement http://microformats.org/wiki/datetime-design-pattern
        return self.publish_date.strftime("%Y-%m-%dT%H:%M:%S%Z")
        
    @models.permalink
    def get_absolute_url(self):
        if self.status == Post.PUBLISHED:
            return ('blog.post_detail', (), {
                'year': self.publish_date.strftime('%Y'),
                'month': self.publish_date.strftime('%b').lower(),
                'day': self.publish_date.strftime('%d'),
                'slug': self.slug
            })
        else:
            return ('blog.draft_post', (), {'post_id': self.id})
        
    def tag_set(self):
        return Tag.objects.get_for_object(self)

    def next_post(self):
        try:
            return Post.objects.published().filter(
                    publish_date__gte=self.publish_date
                ).exclude(pk=self.pk).order_by('publish_date')[0]
        except:
            return None

    def previous_post(self):
        try:
            return Post.objects.published().filter(
                    publish_date__lte=self.publish_date
                ).exclude(pk=self.pk)[0]
        except:
            return None

    def approved_comments(self):
        from comments.models import Comment
        return Comment.objects.approved_for_object(self)