"""
Contribution Serializers

Serializadores para validar y transformar datos de aportes.
"""
from rest_framework import serializers
from datetime import date


class ContributionSerializer(serializers.Serializer):
    """
    Serializer para Aporte
    
    Valida y serializa datos de entrada/salida para aportes.
    """
    
    # Campos de salida (lectura)
    id = serializers.IntegerField(read_only=True)
    affiliate_id = serializers.IntegerField(read_only=True)
    
    # Campos principales
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )
    contribution_date = serializers.DateField()
    payment_method = serializers.ChoiceField(
        choices=['CASH', 'TRANSFER', 'CARD']
    )
    
    # Campos opcionales
    reference_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )
    notes = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    verified = serializers.BooleanField(default=False, read_only=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def validate_contribution_date(self, value):
        """Validación: la fecha no puede ser futura"""
        if value > date.today():
            raise serializers.ValidationError(
                "Contribution date cannot be in the future"
            )
        return value
    
    def validate_amount(self, value):
        """Validación: el monto debe ser positivo"""
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero"
            )
        return value

