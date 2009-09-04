from django.contrib import admin
from glyph.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    
    def admin_link(self, obj):
        if obj.status == Post.PUBLISHED:
            text = "View on site &raquo;"
        else:
            text = "Preview draft &raquo;"
        return obj.permalink(text)
    admin_link.allow_tags = True
    admin_link.short_description = 'Link'
    
    list_display = ('title', 'status', 'publish_date', 'admin_link')
    list_filter = ('status', 'publish_date')
    search_fields = ('tags', 'title', 'body')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
            ('Post details', {
                'fields': ('title', 'body', 'tags')
            }),
            ('Publication options', {
                'fields': ('status', 'publish_date')
            }),
            ('Advanced options', {
                'classes': ('collapse',),
                'fields': ('author', 'summary', 'slug')
            }),
        )

admin.site.register(Post, PostAdmin)