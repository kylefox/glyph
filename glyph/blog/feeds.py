from django.contrib.syndication.feeds import Feed
from glyph.blog.models import Post

class BlogFeed(Feed):
    title = "Kyle Fox: Blog"
    link = "/blog/"
    description = "Latest blog posts from kylefox.ca"

    def items(self):
        return Post.objects.published()[:10]