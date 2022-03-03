from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny


class GETRequestsMixins(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [AllowAny]
