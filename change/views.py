from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from change.filters import ChangeFilter
from change.models import ExchangeOffer
from change.serializers import ProposalSerializer


class ChangeViewSet(ModelViewSet):
    queryset = ExchangeOffer.objects.all()
    serializer_class = ProposalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sender_user", "receiver_user", "status"]
    filterset_class = ChangeFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Предложение успешно создано!",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Обновляет существующее предложение об обмене."""
        change = self.get_object()

        if change.user != request.user:
            raise PermissionDenied(
                detail="У вас нет прав на редактирование этого предложение."
            )

        serializer = self.get_serializer(
            change, data=request.data.get("status"), partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Предложение успешно обновлено.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет предложение."""
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        change = self.get_object()
        if change.user != request.user:
            raise PermissionDenied(
                detail="У вас нет прав на удаление этого предложение."
            )
        change.delete()
        return Response(
            {"message": "Предложение успешно удалено."},
            status=status.HTTP_204_NO_CONTENT,
        )
