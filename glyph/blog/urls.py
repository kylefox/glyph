from django.conf.urls.defaults import *
from glyph.blog import views as blog_views

urlpatterns = patterns('',

    url(r'^archive/$',
        view=blog_views.post_archive,
        name='blog.post_archive'),

    # Post detail
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view=blog_views.post_detail,
        name='blog.post_detail'),
    
    # Preview a draft    
    url(r'^(?P<post_id>\d+)/$', blog_views.post_detail, name='blog.draft_post'),

)