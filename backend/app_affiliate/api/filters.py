"""
API Filters

Filtros personalizados para búsqueda y filtrado de recursos.
"""
from django_filters import rest_framework as filters
from ..infrastructure.repositories.orm_models import AffiliateORM


class AffiliateFilter(filters.FilterSet):
    """
    Filtros para Affiliates
    
    Permite filtrar por:
    - status: Estado exacto (ACTIVE/INACTIVE)
    - document_number: Número de documento exacto
    - full_name: Búsqueda parcial case-insensitive
    """
    
    # Búsqueda parcial en nombre (case-insensitive)
    full_name = filters.CharFilter(
        field_name='full_name',
        lookup_expr='icontains'
    )
    
    # Filtro exacto por status
    status = filters.ChoiceFilter(
        choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')]
    )
    
    # Filtro exacto por documento
    document_number = filters.CharFilter(
        field_name='document_number',
        lookup_expr='exact'
    )
    
    class Meta:
        model = AffiliateORM
        fields = ['status', 'document_number', 'full_name']

