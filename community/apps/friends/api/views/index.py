# DRF
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action

# Serializers
from community.apps.friends.api.serializers import (
    FriendCreateSerializer,
    FriendRequestCreateSerializer,
    FriendRequestSyncSerializer,
    FriendSyncSerializer,
)

# Models
from community.apps.friends.models import Friend, FriendRequest
from community.bases.api import mixins

# Bases
from community.bases.api.viewsets import GenericViewSet
from community.utils.api.response import Response

# Utils
from community.utils.decorators import swagger_decorator


# Main Section
# TODO: DELETE
class FriendRequestViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializers = {
        "default": FriendRequestCreateSerializer,
    }
    queryset = FriendRequest.objects.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(
        **swagger_decorator(
            tag="05. 친구 요청",
            id="친구 요청 생성",
            description="",
            request=FriendRequestCreateSerializer,
            response={201: FriendRequestCreateSerializer},
        ),
        deprecated=True,
    )
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))

    @swagger_auto_schema(
        **swagger_decorator(tag="05. 친구 요청", id="친구 요청 삭제", description="", response={204: "no content"}),
        deprecated=True,
    )
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))

    @swagger_auto_schema(
        **swagger_decorator(
            tag="05. 친구 요청",
            id="친구 요청 싱크",
            description="",
            request=FriendRequestSyncSerializer,
            response={200: FriendRequestSyncSerializer},
        ),
        deprecated=True,
    )
    @action(detail=False, methods=["post"])
    def sync(self, request):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))

        # friend_request_id = request.data.pop("id", None)
        # friend_request = FriendRequest.objects.filter(id=friend_request_id).first()

        # if not friend_request:
        #     raise ParseError("존재하지 않는 친구 요청 데이터")

        # serializer = FriendRequestSyncSerializer(instance=friend_request, data=request.data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(
        #         status=status.HTTP_200_OK,
        #         code=200,
        #         message="ok",
        #         data=FriendRequestSyncSerializer(instance=friend_request, context={"request": request}).data,
        #     )


class FriendViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializers = {
        "default": FriendCreateSerializer,
    }
    queryset = Friend.objects.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(
        **swagger_decorator(
            tag="05. 친구",
            id="친구 생성",
            description="",
            request=FriendCreateSerializer,
            response={201: FriendCreateSerializer},
        ),
        deprecated=True,
    )
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))

    @swagger_auto_schema(
        **swagger_decorator(tag="05. 친구", id="친구 삭제", description="", response={204: "no content"}),
        deprecated=True,
    )
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))

    @swagger_auto_schema(
        **swagger_decorator(
            tag="05. 친구",
            id="친구 싱크",
            description="",
            request=FriendSyncSerializer,
            response={200: FriendSyncSerializer},
        ),
        deprecated=True,
    )
    @action(detail=False, methods=["post"])
    def sync(self, request):
        return Response(status=status.HTTP_200_OK, code=200, message=_("ok"))
        # friend_id = request.data.pop("id", None)
        # friend = Friend.objects.filter(id=friend_id).first()

        # if not friend:
        #     raise ParseError("존재하지 않는 친구 데이터")

        # serializer = FriendSyncSerializer(instance=friend, data=request.data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(
        #         status=status.HTTP_200_OK,
        #         code=200,
        #         message="ok",
        #         data=FriendSyncSerializer(instance=friend, context={"request": request}).data,
        #     )
