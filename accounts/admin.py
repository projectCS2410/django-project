from django.contrib import admin

from .models import FilmComment


@admin.register(FilmComment)
class FilmCommentAdmin(admin.ModelAdmin):
    list_display = ('film_title', 'user', 'created_at')
    list_filter = ('film_title', 'created_at')
    search_fields = ('film_title', 'text', 'user__username')
    ordering = ('-created_at',)
