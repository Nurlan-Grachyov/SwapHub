from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]


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
        obj = self.get_object()

        new_status = request.data.get('status')

        if new_status and new_status in dict(obj.STATUS_CHOICES):
            obj.status = new_status
            obj.save(update_fields=['status'])

            return Response({"message": f"Статус успешно обновлен на {new_status}"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Можно обновить только статус."}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет предложение."""
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        change = self.get_object()
        change.delete()
        return Response(
            {"message": "Предложение успешно удалено."},
            status=status.HTTP_204_NO_CONTENT,
        )
