from rest_framework import viewsets

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        # Set the rabbithole owner to the request user.
        global serializer_class
        serializer_class.save(owner=request.user)

    def filter_queryset(self, queryset):
        # Only return RabbitHoles that belong to the querying user 
        user = self.request.user
        return queryset.filter(owner=user)
    
    def delete(self, request, *args, **kwargs):
        # Check if the user is a superuser 
        if request.user.is_superuser:
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # If the user is not a superuser return permission denied response
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()