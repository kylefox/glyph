from django.conf.urls.defaults import *
from glyph.notes import views as notes_views

urlpatterns = patterns('',

    url(r'^archive/$',
        view=notes_views.archive,
        name='notes.archive'),

    # Note detail
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view=notes_views.note_detail,
        name='notes.note_detail'),

)