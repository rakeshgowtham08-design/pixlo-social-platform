from django.contrib import admin
from .models import Profile, Follow, Post, Like, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "bio")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at")
    search_fields = ("author__username", "caption")
    list_filter = ("created_at",)

admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
