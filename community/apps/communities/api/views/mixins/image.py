# DRF
# Third Party
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView

# Serializers
from community.apps.communities.api.serializers import (
    CommunityBannerImageSerializer,
    CommunityBannerImageUpdateSerializer,
    ProfileImageUpdateSerializer,
)

# Function
from community.apps.communities.models.mixins.image import default_banner_image_path

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator
from community.utils.exception_handlers import PermissionDenied


class CommunityImageViewMixin(GenericAPIView):
    @swagger_auto_schema(
        **swagger_decorator(
            tag="02. 커뮤니티 - 어드민",
            id="프로필 이미지 수정",
            description="",
            request=ProfileImageUpdateSerializer,
            response={200: ProfileImageUpdateSerializer},
        )
    )
    @action(detail=True, methods=["patch"], url_path="profile-image", url_name="community_profile_image")
    def community_profile_image(self, request, pk=None):
        user = request.user
        community = self.get_object()
        data = request.data
        if community.user == user:
            serializer = ProfileImageUpdateSerializer(instance=community, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_200_OK, code=200, message="ok", data=serializer.data)
        raise PermissionDenied("community 관리자가 아닙니다.")

    @swagger_auto_schema(
        **swagger_decorator(
            tag="02. 커뮤니티 - 어드민",
            id="배너 이미지 수정",
            description="",
            request=CommunityBannerImageUpdateSerializer,
            response={200: CommunityBannerImageUpdateSerializer},
        )
    )
    @action(detail=True, methods=["patch"], url_path="banner-image", url_name="community_banner_image")
    def community_banner_image(self, request, pk=None):
        user = request.user
        community = self.get_object()
        data = request.data
        if community.user == user:
            serializer = CommunityBannerImageUpdateSerializer(instance=community, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_200_OK, code=200, message="ok", data=serializer.data)
        raise PermissionDenied("community 관리자가 아닙니다.")

    @swagger_auto_schema(
        **swagger_decorator(
            tag="02. 커뮤니티 - 어드민",
            id="배너 이미지 초기화",
            description="",
            request=no_body,
            response={200: CommunityBannerImageSerializer},
        )
    )
    @action(detail=True, methods=["post"], url_path="banner-image/reset", url_name="community_banner_image_reset")
    def community_banner_image_reset(self, request, pk=None):
        community = self.get_object()
        default_banner_img_path = default_banner_image_path()
        community.banner_image = None
        community.banner_image_url = default_banner_img_path
        community.save()
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message="ok",
            data=CommunityBannerImageSerializer(instance=community, context={"request": request}).data,
        )
