"""
Affiliate API Views

Endpoints REST para gestionar afiliados.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ...application.services import (
    CreateAffiliateService,
    UpdateAffiliateService,
    ChangeAffiliateStatusService,
    GetAffiliateSummaryService,
)
from ...infrastructure.repositories import (
    DjangoAffiliateRepository,
    DjangoContributionRepository,
)
from ...domain.exceptions import (
    AffiliateAlreadyExistsError,
    AffiliateNotFoundError,
    DomainException,
)
from ..serializers import (
    AffiliateSerializer,
    AffiliateUpdateSerializer,
    AffiliateStatusSerializer,
    AffiliateSummarySerializer,
)
from ..filters import AffiliateFilter


class AffiliateViewSet(viewsets.ViewSet):
    """
    ViewSet para Affiliates
    
    Endpoints:
    - GET /api/affiliates/ - Lista paginada con filtros
    - POST /api/affiliates/ - Crear afiliado
    - GET /api/affiliates/{id}/ - Detalle de afiliado
    - PUT /api/affiliates/{id}/ - Actualizar afiliado
    - PATCH /api/affiliates/{id}/status/ - Cambiar estado
    - GET /api/affiliates/{id}/summary/ - Resumen de aportes
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inyección de dependencias
        self.affiliate_repository = DjangoAffiliateRepository()
        self.contribution_repository = DjangoContributionRepository()
    
    def list(self, request):
        """
        GET /api/affiliates/
        
        Lista afiliados con paginación y filtros.
        
        Query params opcionales:
        - page: Número de página
        - page_size: Elementos por página
        - status: Filtrar por estado (ACTIVE/INACTIVE)
        - document_number: Filtrar por documento
        - full_name: Búsqueda parcial en nombre
        """
        # Obtener parámetros de query
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        # Construir filtros
        filters = {}
        if 'status' in request.query_params:
            filters['status'] = request.query_params['status']
        if 'document_number' in request.query_params:
            filters['document_number'] = request.query_params['document_number']
        if 'full_name' in request.query_params:
            filters['full_name'] = request.query_params['full_name']
        
        # Obtener afiliados del repositorio
        affiliates, total_count = self.affiliate_repository.list_all(
            page=page,
            page_size=page_size,
            filters=filters
        )
        
        # Serializar respuesta
        serializer = AffiliateSerializer(affiliates, many=True)
        
        # Formato de paginación
        return Response({
            'count': total_count,
            'next': page + 1 if (page * page_size) < total_count else None,
            'previous': page - 1 if page > 1 else None,
            'results': serializer.data
        })
    
    def create(self, request):
        """
        POST /api/affiliates/
        
        Crea un nuevo afiliado.
        
        Body (JSON):
        {
            "full_name": "Juan Pérez",
            "document_type": "CC",
            "document_number": "123456789",
            "email": "juan@example.com",
            "status": "ACTIVE" (opcional),
            "phone_number": "..." (opcional),
            "address": "..." (opcional),
            "notes": "..." (opcional)
        }
        """
        # Validar datos de entrada
        serializer = AffiliateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Ejecutar caso de uso
            service = CreateAffiliateService(self.affiliate_repository)
            affiliate = service.execute(serializer.validated_data)
            
            # Serializar respuesta
            response_serializer = AffiliateSerializer(affiliate)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        except AffiliateAlreadyExistsError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DomainException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """
        GET /api/affiliates/{id}/
        
        Obtiene el detalle de un afiliado.
        """
        affiliate = self.affiliate_repository.find_by_id(int(pk))
        
        if not affiliate:
            return Response(
                {'error': 'Affiliate not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AffiliateSerializer(affiliate)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        PUT /api/affiliates/{id}/
        
        Actualiza un afiliado completo.
        """
        # Validar datos
        serializer = AffiliateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Ejecutar caso de uso
            service = UpdateAffiliateService(self.affiliate_repository)
            affiliate = service.execute(int(pk), serializer.validated_data)
            
            # Serializar respuesta
            response_serializer = AffiliateSerializer(affiliate)
            return Response(response_serializer.data)
        
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
    
    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        """
        PATCH /api/affiliates/{id}/status/
        
        Cambia el estado de un afiliado.
        
        Body (JSON):
        {
            "status": "ACTIVE" | "INACTIVE"
        }
        """
        # Validar datos
        serializer = AffiliateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Ejecutar caso de uso
            service = ChangeAffiliateStatusService(self.affiliate_repository)
            affiliate = service.execute(
                int(pk),
                serializer.validated_data['status']
            )
            
            # Serializar respuesta
            response_serializer = AffiliateSerializer(affiliate)
            return Response(response_serializer.data)
        
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
    
    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """
        GET /api/affiliates/{id}/summary/
        
        Obtiene el resumen estadístico de aportes del afiliado.
        
        Respuesta:
        {
            "affiliate": {
                "full_name": "...",
                "document_number": "...",
                "status": "..."
            },
            "total_contributions": 123456.78,
            "contributions_count": 10,
            "last_contribution_date": "2025-11-18"
        }
        """
        try:
            # Ejecutar caso de uso
            service = GetAffiliateSummaryService(
                self.affiliate_repository,
                self.contribution_repository
            )
            summary = service.execute(int(pk))
            
            # Serializar respuesta
            serializer = AffiliateSummarySerializer(summary)
            return Response(serializer.data)
        
        except AffiliateNotFoundError:
            return Response(
                {'error': 'Affiliate not found'},
                status=status.HTTP_404_NOT_FOUND
            )

