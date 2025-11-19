"""
ORM Models (Django)

Modelos de Django que mapean a las tablas de la base de datos.
Estos NO contienen lógica de negocio, solo persistencia.
"""
from django.db import models


class AffiliateORM(models.Model):
    """
    Modelo ORM: Afiliado
    
    Mapea la tabla 'affiliates' en PostgreSQL.
    Solo responsable de la persistencia, sin lógica de negocio.
    """
    
    # Choices para document_type
    class DocumentTypeChoices(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        CE = 'CE', 'Cédula de Extranjería'
        NIT = 'NIT', 'Número de Identificación Tributaria'
    
    # Choices para status
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Activo'
        INACTIVE = 'INACTIVE', 'Inactivo'
    
    # Campos principales
    full_name = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=10,
        choices=DocumentTypeChoices.choices
    )
    document_number = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    
    # Campos opcionales
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'affiliates'
        verbose_name = 'Affiliate'
        verbose_name_plural = 'Affiliates'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document_number']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.document_number})"


class ContributionORM(models.Model):
    """
    Modelo ORM: Aporte
    
    Mapea la tabla 'contributions' en PostgreSQL.
    """
    
    # Choices para payment_method
    class PaymentMethodChoices(models.TextChoices):
        CASH = 'CASH', 'Efectivo'
        TRANSFER = 'TRANSFER', 'Transferencia'
        CARD = 'CARD', 'Tarjeta'
    
    # Relación con Affiliate
    affiliate = models.ForeignKey(
        AffiliateORM,
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    
    # Campos principales
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contribution_date = models.DateField()
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices
    )
    
    # Campos opcionales
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contributions'
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
        ordering = ['-contribution_date', '-created_at']
        indexes = [
            # Índice compuesto: optimiza consultas por afiliado y fecha
            models.Index(fields=['affiliate', 'contribution_date']),
            models.Index(fields=['contribution_date']),
            models.Index(fields=['verified']),
        ]
    
    def __str__(self):
        return f"Contribution {self.amount} on {self.contribution_date}"

