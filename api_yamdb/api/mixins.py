from rest_framework import mixins, viewsets


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет: получение списка объектов, создание и удаление."""
