from community.bases.admin import Admin


class ReportAdmin(Admin):
    list_display = ("post", "comment", "profile", "content")
    fieldsets = (("정보", {"fields": ("post", "comment", "profile", "content")}),)


class ReportChoiceAdmin(Admin):
    list_display = ("community", "content")
    fieldsets = (("정보", {"fields": ("community", "content")}),)
    add_fieldsets = (("정보", {"fields": ("community", "content")}),)


class ReportGroupAdmin(Admin):
    list_display = (
        "community",
        "post",
        "comment",
        "contents",
        "user",
        "profile",
        "username",
        "profile_is_banned",
        "profile_is_banned",
        "profile_is_deactivated",
        "is_deactivated",
        "deactivated_at",
        "reported_count",
    )
    search_fields = ()
    list_filter = ()
