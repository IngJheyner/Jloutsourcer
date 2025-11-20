"""
Affiliate Serializers

Serializadores para validar y transformar datos de afiliados.
"""
from rest_framework import serializers


class AffiliateSerializer(serializers.Serializer):
    """
    Serializer para Afiliado
    
    Valida y serializa datos de entrada/salida para afiliados.
    """
    
    # Campos de salida (lectura)
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=255)
    document_type = serializers.ChoiceField(
        choices=['CC', 'CE', 'NIT']
    )
    document_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    status = serializers.ChoiceField(
        choices=['ACTIVE', 'INACTIVE'],
        default='ACTIVE'
    )
    
    # Campos opcionales
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True
    )
    address = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    notes = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def validate_full_name(self, value):
        """Validación personalizada para nombre"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Full name must be at least 3 characters long"
            )
        return value.strip()
    
    def validate_document_number(self, value):
        """Validación personalizada para número de documento"""
        if not value.strip():
            raise serializers.ValidationError(
                "Document number cannot be empty"
            )
        return value.strip()


class AffiliateUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualización parcial de afiliado
    
    Todos los campos son opcionales para PATCH.
    """
    
    full_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True
    )
    address = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    notes = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )


class AffiliateStatusSerializer(serializers.Serializer):
    """
    Serializer para cambio de estado de afiliado
    
    Solo permite cambiar el campo status.
    """
    
    status = serializers.ChoiceField(
        choices=['ACTIVE', 'INACTIVE']
    )


class AffiliateSummarySerializer(serializers.Serializer):
    """
    Serializer para el resumen de aportes de un afiliado
    
    Formato de salida del endpoint /summary/
    """
    
    affiliate = serializers.DictField()
    total_contributions = serializers.FloatField()
    contributions_count = serializers.IntegerField()
    last_contribution_date = serializers.DateField(allow_null=True)

