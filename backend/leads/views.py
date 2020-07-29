from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from leads import serializers
from leads.models import Lead
from leads.permissions import CustomUserPermission


class LeadViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin):
    """
    Manage leads
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (CustomUserPermission, )
    #permission_classes = (IsAuthenticated, )

    queryset = Lead.objects.all()
    serializer_class = serializers.LeadSerializer

    def get_queryset(self):
        """
        Return objects for the current authenticated user
        """
        return self.queryset.order_by('-name')
    
    def perform_create(self, serializer):
        """
        Create a lead
        """
        serializer.save(created_by=self.request.user)