from django.contrib.sitemaps import Sitemap
from glyph.notes.models import Note

class NoteSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6

    def items(self):
        return Note.objects.all()

    def lastmod(self, obj):
        return obj.publish_date