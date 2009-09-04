from django.views.generic.date_based import object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from glyph.blog.models import Post

def post_detail(request, *args, **kwargs):
    kwargs.update({
        'queryset': Post.objects.published(),
        'date_field': 'publish_date',
        'slug_field': 'slug',
        'template_object_name': 'post',
    })
    return object_detail(request, **kwargs)
    
def post_archive(request):
    posts = Post.objects.published()
    return render_to_response('blog/archive.html', {'posts':posts},
        context_instance=RequestContext(request))