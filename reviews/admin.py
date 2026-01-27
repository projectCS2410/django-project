from django.contrib import admin
from .models import Item, Review

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('item__title', 'user__username', 'text')
