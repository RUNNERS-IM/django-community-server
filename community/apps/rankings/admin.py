# Django
from django.contrib import admin

# Inlines
from community.apps.rankings.inline import CommunityRankingInline, PostRankingInline

# Models
from community.apps.rankings.models import CommunityRanking, PostRanking, RankingGroup

# Bases
from community.bases.admin import Admin


# Main Section
from config._admin.decorators import register_custom_admin
@register_custom_admin(RankingGroup)
class RankingGroupAdmin(Admin):
    list_display = ("model_type", "ranking_type", "is_active")
    search_fields = ()
    list_filter = ()

    fieldsets = (
        ("1. 정보", {"fields": ("model_type", "ranking_type")}),
        ("2. 활성화 여부", {"fields": ("is_active",)}),
    )

    inlines = (CommunityRankingInline, PostRankingInline)


from config._admin.decorators import register_custom_admin
@register_custom_admin(CommunityRanking)
class CommunityRankingAdmin(Admin):
    list_display = (
        "ranking_group",
        "prev_ranking_group",
        "community",
        "rank",
        "old_rank",
        "point",
        "rank_change",
        "is_active",
    )
    search_fields = ()
    list_filter = ()

    fieldsets = (
        (
            "1. 정보",
            {
                "fields": (
                    "ranking_group",
                    "prev_ranking_group",
                    "community",
                    "rank",
                    "old_rank",
                    "point",
                    "rank_change",
                )
            },
        ),
        ("2. 활성화 여부", {"fields": ("is_active",)}),
    )


from config._admin.decorators import register_custom_admin
@register_custom_admin(PostRanking)
class PostRankingAdmin(Admin):
    list_display = (
        "ranking_group",
        "prev_ranking_group",
        "community",
        "post",
        "board",
        "rank",
        "old_rank",
        "point",
        "rank_change",
        "is_active",
    )
    search_fields = ()
    list_filter = ()

    fieldsets = (
        (
            "1. 정보",
            {
                "fields": (
                    "ranking_group",
                    "prev_ranking_group",
                    "community",
                    "post",
                    "board",
                    "rank",
                    "old_rank",
                    "point",
                    "rank_change",
                )
            },
        ),
        ("2. 활성화 여부", {"fields": ("is_active",)}),
    )
