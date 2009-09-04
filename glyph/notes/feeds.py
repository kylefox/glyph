from django.contrib.syndication.feeds import Feed
from glyph.notes.models import Note

class NoteFeed(Feed):
    title = "Kyle Fox: Notes"
    link = "/notes/"
    description = "Notes and other miscellany from kylefox.ca"

    def items(self):
        return Note.objects.all()[:15]