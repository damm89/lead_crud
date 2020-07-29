from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for lead objects
    """
    class Meta:
        model = Lead
        fields = ('id', 'name', 'created_by', 'credit_score')
        read_only_fields = ('id', 'created_by')