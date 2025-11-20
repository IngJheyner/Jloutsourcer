"""
Contribution API Views

Endpoints REST para gestionar aportes.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from ...application.services import RegisterContributionService
from ...infrastructure.repositories import (
    DjangoAffiliateRepository,
    DjangoContributionRepository,
)
from ...domain.exceptions import (
    AffiliateNotFoundError,
    DomainException,
)
from ..serializers import ContributionSerializer


class ContributionViewSet(viewsets.ViewSet):
    """
    ViewSet para Contributions
    
    Endpoints:
    - GET /api/affiliates/{affiliate_id}/contributions/ - Lista aportes
    - POST /api/affiliates/{affiliate_id}/contributions/ - Crear aporte
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inyección de dependencias
        self.affiliate_repository = DjangoAffiliateRepository()
        self.contribution_repository = DjangoContributionRepository()
    
    def list(self, request, affiliate_pk=None):
        """
        GET /api/affiliates/{affiliate_id}/contributions/
        
        Lista aportes de un afiliado ordenados por fecha DESC.
        
        Query params opcionales:
        - page: Número de página
        - page_size: Elementos por página
        """
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        # Obtener aportes del repositorio
        contributions, total_count = self.contribution_repository.find_by_affiliate(
            affiliate_id=int(affiliate_pk),
            page=page,
            page_size=page_size
        )
        
        # Serializar respuesta
        serializer = ContributionSerializer(contributions, many=True)
        
        return Response({
            'count': total_count,
            'next': page + 1 if (page * page_size) < total_count else None,
            'previous': page - 1 if page > 1 else None,
            'results': serializer.data
        })
    
    def create(self, request, affiliate_pk=None):
        """
        POST /api/affiliates/{affiliate_id}/contributions/
        
        Registra un nuevo aporte para el afiliado.
        
        Body (JSON):
        {
            "amount": 50000.00,
            "contribution_date": "2025-11-18",
            "payment_method": "CASH" | "TRANSFER" | "CARD",
            "reference_number": "..." (opcional),
            "notes": "..." (opcional)
        }
        """
        # Validar datos de entrada
        serializer = ContributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Ejecutar caso de uso
            service = RegisterContributionService(
                self.affiliate_repository,
                self.contribution_repository
            )
            contribution = service.execute(
                int(affiliate_pk),
                serializer.validated_data
            )
            
            # Serializar respuesta
            response_serializer = ContributionSerializer(contribution)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        except AffiliateNotFoundError:
            return Response(
                {'error': 'Affiliate not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except DomainException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

