from django.contrib import admin

from .models import UserProfile,SavedResource,TopicFollow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'about', 'user_type', 'last_updated')
search_fields = ('user', 'about')


class SavedResourceAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'saved_at')
    date_hierarchy = 'saved_at'

class TopicFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'followed_at')
    date_hierarchy = 'followed_at'



admin.site.register(SavedResource, SavedResourceAdmin)
admin.site.register(TopicFollow, TopicFollowAdmin)    