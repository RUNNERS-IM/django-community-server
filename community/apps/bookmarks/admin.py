# Django
from django.contrib import admin

# Models
from community.apps.bookmarks.models.index import PostBookmark

# Bases
from community.bases.admin import Admin


# Main Section
class PostBookmarkAdmin(Admin):
    list_display = ("post", "user")
    search_fields = ("post__title", "user__email")
    readonly_fields = ("post", "user")
