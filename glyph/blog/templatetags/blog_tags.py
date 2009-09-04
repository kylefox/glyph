from django import template
from template_utils.nodes import GenericContentNode

class LatestPostsNode(GenericContentNode):

    def _get_query_set(self, *args, **kwargs):
        from glyph.blog.models import Post
        return Post.objects.published()
        
def get_latest_posts(parser, token):
    """
    Retrieves the latest ``num`` objects from a given model, in that
    model's default ordering, and stores them in a context variable.

    Syntax::

        {% get_latest_objects [app_name].[model_name] [num] as [varname] %}

    Example::

        {% get_latest_objects comments.freecomment 5 as latest_comments %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits [3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return LatestPostsNode(bits[1], bits[2], bits[4])
    
register = template.Library()
register.tag('get_latest_posts', get_latest_posts)