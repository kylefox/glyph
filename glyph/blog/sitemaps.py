from django.contrib.sitemaps import Sitemap
from glyph.blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.modified_at