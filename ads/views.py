from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ads.filters import AdsFilter
from ads.models import Product
from ads.paginators import AdsPaginator
from ads.serializers import AdSerializer


class AdsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdsPaginator
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "condition"]
    filterset_class = AdsFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Продукт успешно создан!",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Обновляет существующее объявление."""
        product = self.get_object()

        if product.user != request.user:
            raise PermissionDenied(
                detail="У вас нет прав на редактирование этого объявления."
            )

        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Объявление успешно обновлено.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет объявление."""
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.user != request.user:
            raise PermissionDenied(
                detail="У вас нет прав на удаление этого объявления."
            )
        product.delete()
        return Response(
            {"message": "Объявление успешно удалено."},
            status=status.HTTP_204_NO_CONTENT,
        )
