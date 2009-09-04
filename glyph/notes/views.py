from django.views.generic.date_based import object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from glyph.notes.models import Note

def note_detail(request, *args, **kwargs):
    kwargs.update({
        'queryset': Note.objects.all(),
        'date_field': 'publish_date',
        'slug_field': 'slug',
        'template_object_name': 'note',
    })
    return object_detail(request, **kwargs)
    
def archive(request):
    notes = Note.objects.all()
    return render_to_response('notes/archive.html', {'notes':notes},
        context_instance=RequestContext(request))
