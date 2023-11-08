# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework.serializers import SerializerMetaclass

# Third Party
from drf_yasg import openapi


# Main Section
def swagger_decorator(
    tag,
    id=None,
    description='',
    request=None,
    response=None,
):

    data = dict(
        operation_id=_(id),
        operation_description=_(description),
        tags=[tag],
        responses={}
    )

    if request:
        data['request_body'] = request

    for response_code in response.keys():
        message = None
        serializer = None

        if isinstance(response[response_code], str):
            message = response[response_code]
            data['responses'][response_code] = openapi.Response(_(message))

        elif isinstance(response[response_code], SerializerMetaclass):
            serializer = response[response_code]
            data['responses'][response_code] = openapi.Response(_('ok'), serializer)

        elif isinstance(response[response_code], tuple) or isinstance(response[response_code], list):
            print(response[response_code])
            for value in response[response_code]:
                if isinstance(value, str):
                    message = value
                elif isinstance(value, SerializerMetaclass):
                    serializer = value

            data['responses'][response_code] = openapi.Response(_(message), serializer)

    return data
