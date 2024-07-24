from django.contrib import admin
from django.utils.html import format_html
from .models import Contributor, Score, Badge

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('username', 'github_id', 'display_avatar')
    search_fields = ('username',)
    filter_horizontal = ('badges',)

    def display_avatar(self, obj):
        if obj.avatar_url:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar_url)
        return 'No image'
    
    display_avatar.short_description = 'Avatar'

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('rank', 'username', 'score', 'contributor')
    search_fields = ('username', 'contributor__username')
    list_filter = ('rank',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return format_html('<span>No image</span>')

    image_tag.short_description = 'Image'
