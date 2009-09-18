from django.contrib import admin
from glyph.notes.models import Note

class NoteAdmin(admin.ModelAdmin):
    
    def admin_link(self, obj):
        return obj.permalink("View")
        
    admin_link.allow_tags = True
    admin_link.short_description = 'Link'
    
    def get_content(self, obj):
        return obj.body
    get_content.allow_tags = True
    get_content.short_description = "Note"
    
    list_display = ('title', 'tags', 'publish_date', 'admin_link')
    list_filter = ('publish_date',)
    search_fields = ('tags', 'title', 'body')
    prepopulated_fields = {"slug": ("body",)}

admin.site.register(Note, NoteAdmin)