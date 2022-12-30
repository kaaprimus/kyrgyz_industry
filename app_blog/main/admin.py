from django.contrib import admin
from .models import *

admin.site.register(Projects)
admin.site.register(PhotosProject)
admin.site.register(GalleryProject)

admin.site.register(Contests)
admin.site.register(GalleryNews)
admin.site.register(HotNews)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Language')