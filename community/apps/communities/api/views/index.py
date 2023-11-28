# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Mixins
from community.apps.communities.api.views.mixins import CommunityImageViewMixin, CommunityBoardGroupViewMixin, \
    CommunityPostViewMixin, CommunityDashboardViewMixin

# Filters
from community.apps.communities.api.views.filters import CommunitiesFilter, CommunityFilter

# Utils
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response
from community.utils.searches import AdvancedSearchFilter

# Models
from community.apps.communities.models import Community
from community.apps.profiles.models import Profile

# Serializers
from community.apps.communities.api.serializers import CommunityListSerializer, CommunityRetrieveSerializer, \
    CommunityUpdateAdminSerializer


# Main Section
class CommunityViewSet(mixins.RetrieveModelMixin,
                       CommunityPostViewMixin,
                       CommunityDashboardViewMixin,
                       GenericViewSet):
    serializers = {
        'default': CommunityRetrieveSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommunityFilter
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='커뮤니티 객체 조회',
                                             description='## < 커뮤니티 객체 조회 API 입니다. >',
                                             response={200: CommunityRetrieveSerializer}
                                             ))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        user = request.user

        if user.id:
            profile = instance.profiles.filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(community=instance, user=user)

            instance.create_community_visit(profile)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=serializer.data
        )


class CommunitiesViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    serializers = {
        'default': CommunityListSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (AdvancedSearchFilter, DjangoFilterBackend)
    ordering_fields = ('created', 'order')
    filterset_class = CommunitiesFilter
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='커뮤니티 리스트 조회',
                                             description='## < 커뮤니티 리스트 조회 API 입니다. > \n'
                                                         '### ordering : `created (생성순)` \n'
                                                         '### `depth` : depth 로 필터링 가능합니다.\n'
                                                         '### `community_id` : community_id 로 필터링 가능합니다.\n',
                                             response={200: CommunityListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommunityAdminViewSet(mixins.UpdateModelMixin,
                            CommunityImageViewMixin,
                            CommunityBoardGroupViewMixin,
                            GenericViewSet):
    serializers = {
        'partial_update': CommunityUpdateAdminSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티 - 어드민',
                                             id='커뮤니티 수정',
                                             description='## < 커뮤니티 수정 API 입니다. >',
                                             request=CommunityUpdateAdminSerializer,
                                             response={200: CommunityUpdateAdminSerializer}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
