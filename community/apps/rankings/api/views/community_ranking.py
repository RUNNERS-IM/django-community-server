# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# DRF
from rest_framework.filters import OrderingFilter

# Serializers
from community.apps.rankings.api.serializers import CommunityRankingListSerializer

# Filters
from community.apps.rankings.api.views.filters import RankingFilter

# Models
from community.apps.rankings.models import CommunityRanking

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator


# Main Section
class CommunityRankingsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {
        "default": CommunityRankingListSerializer,
    }
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RankingFilter
    ordering_fields = ["created"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None
        queryset = CommunityRanking.objects.filter(community=self.kwargs["community_pk"])
        return queryset

    @swagger_auto_schema(
        **swagger_decorator(
            tag="02. 커뮤니티",
            id="커뮤니티 랭킹 리스트 조회",
            description="## < 커뮤니티 랭킹 리스트 조회 API 입니다. >\n" "### `ranking_type`: live, weekly, monthly",
            response={200: CommunityRankingListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
