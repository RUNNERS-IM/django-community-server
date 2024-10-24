# DRF
# Third Party
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action

# Serializers
from community.apps.bans.api.serializers import UserBanSyncSerializer
from community.utils.api.response import Response

# Utils
from community.utils.decorators import swagger_decorator


# Main Section
class BanSyncViewMixin:
    @swagger_auto_schema(
        **swagger_decorator(tag="11. 밴", id="밴 싱크", description="", request=UserBanSyncSerializer, response={200: "ok"})
    )
    @action(detail=True, methods=["post"])
    def sync(self, request, *args, **kwargs):
        # ban = self.get_object()
        # serializer = UserBanSyncSerializer(instance=ban, data=request.data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
            return Response(
                status=status.HTTP_200_OK, code=200, message="ok"
            )
