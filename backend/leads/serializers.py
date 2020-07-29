from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for lead objects
    """
    class Meta:
        model = Lead
        fields = ('id', 'name')
        read_only_fields = ('id',)