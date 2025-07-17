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
        """
        Creates a new exchange offer.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Proposal successfully created!",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates the status of an existing exchange offer.
        """
        obj = self.get_object()

        new_status = request.data.get("status")

        if new_status and new_status in dict(obj.STATUS_CHOICES):
            obj.status = new_status
            obj.save(update_fields=["status"])

            return Response(
                {"message": f"Status successfully updated to {new_status}"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Only status can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Performs a partial update on the proposal.
        """
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Prevents deletion of an exchange offer.
        """
        return Response(
            {"detail": "Deletion is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
