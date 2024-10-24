# TODO: 삭제
# DRF
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

# Serializers
from community.apps.bans.api.serializers import (
    UserBanCreateSerializer,
    UserBanSyncSerializer,
)

# Mixins
from community.apps.bans.api.views.mixins import BanSyncViewMixin

# Models
from community.apps.bans.models import UserBan
from community.bases.api import mixins

# Bases
from community.bases.api.viewsets import GenericViewSet
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator


# Main Section
class BanViewSet(mixins.CreateModelMixin, BanSyncViewMixin, GenericViewSet):
    serializers = {
        "default": UserBanCreateSerializer,
        "sync": UserBanSyncSerializer,
    }
    queryset = UserBan.objects.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(
        **swagger_decorator(
            tag="11. 밴", id="밴 생성", description="", request=UserBanCreateSerializer, response={201: "ok"}
        ), deprecated=True
    )
    def create(self, request, *args, **kwargs):
        # return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, code=200, message="ok")
