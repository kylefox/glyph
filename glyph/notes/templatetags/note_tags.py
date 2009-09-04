from django import template
from template_utils.nodes import GenericContentNode

class LatestNotesNode(GenericContentNode):

    def _get_query_set(self, *args, **kwargs):
        from glyph.notes.models import Note
        return Note.objects.all().order_by('-publish_date')
        
def get_latest_notes(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits [3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return LatestNotesNode(bits[1], bits[2], bits[4])
    
register = template.Library()
register.tag('get_latest_notes', get_latest_notes)