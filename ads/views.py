from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ads.filters import AdsFilter
from ads.models import Ad
from ads.paginators import AdsPaginator
from ads.serializers import AdSerializer


class AdsViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdsPaginator
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "condition"]
    filterset_class = AdsFilter

    def create(self, request, *args, **kwargs):
        """
        Creates a new advertisement.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Product successfully created!",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing advertisement.
        """
        product = self.get_object()

        if product.user != request.user:
            raise PermissionDenied(
                detail="You do not have permissions to edit this advertisement."
            )

        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Advertisement successfully updated.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an advertisement.
        """
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an advertisement.
        """
        product = self.get_object()
        if product.user != request.user:
            raise PermissionDenied(
                detail="You do not have permissions to delete this advertisement."
            )
        product.delete()
        return Response(
            {"message": "Advertisement successfully deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
