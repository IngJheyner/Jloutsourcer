"""
Django Affiliate Repository

Implementación concreta del repositorio de afiliados usando Django ORM.
Traduce entre entidades del dominio (Affiliate) y modelos ORM (AffiliateORM).
"""
from typing import List, Optional
from django.core.paginator import Paginator
from django.db.models import Q

from ...domain.interfaces import IAffiliateRepository
from ...domain.models import Affiliate, Email, DocumentType, AffiliateStatus
from .orm_models import AffiliateORM


class DjangoAffiliateRepository(IAffiliateRepository):
    """
    Repositorio de afiliados usando Django ORM
    
    Implementa la interfaz IAffiliateRepository definida en el dominio.
    """
    
    def save(self, affiliate: Affiliate) -> Affiliate:
        """
        Guarda o actualiza un afiliado en la base de datos
        
        Flujo:
        1. Si tiene ID → buscar el registro existente
        2. Convertir Affiliate (dominio) → AffiliateORM (Django)
        3. Guardar en PostgreSQL
        4. Convertir de vuelta: AffiliateORM → Affiliate
        """
        if affiliate.id:
            # Actualizar existente
            try:
                orm_model = AffiliateORM.objects.get(pk=affiliate.id)
                orm_model = self._to_orm(affiliate, orm_model)
            except AffiliateORM.DoesNotExist:
                # Si no existe, crear nuevo
                orm_model = self._to_orm(affiliate)
        else:
            # Crear nuevo
            orm_model = self._to_orm(affiliate)
        
        orm_model.save()
        return self._to_domain(orm_model)
    
    def find_by_id(self, affiliate_id: int) -> Optional[Affiliate]:
        """
        Busca un afiliado por su ID
        
        Returns:
            Affiliate si existe, None si no
        """
        try:
            orm_model = AffiliateORM.objects.get(pk=affiliate_id)
            return self._to_domain(orm_model)
        except AffiliateORM.DoesNotExist:
            return None
    
    def find_by_document(self, document_number: str) -> Optional[Affiliate]:
        """
        Busca un afiliado por número de documento
        
        Usa el índice en document_number para búsqueda rápida
        """
        try:
            orm_model = AffiliateORM.objects.get(document_number=document_number)
            return self._to_domain(orm_model)
        except AffiliateORM.DoesNotExist:
            return None
    
    def exists_by_document(self, document_number: str) -> bool:
        """
        Verifica si existe un afiliado con ese documento
        
        Más eficiente que find_by_document() porque no carga todos los campos
        """
        return AffiliateORM.objects.filter(document_number=document_number).exists()
    
    def list_all(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[dict] = None
    ) -> tuple[List[Affiliate], int]:
        """
        Lista afiliados con paginación y filtros
        
        Args:
            page: Número de página (base 1)
            page_size: Elementos por página
            filters: Diccionario con filtros opcionales:
                - status: ACTIVE o INACTIVE
                - full_name: Búsqueda parcial (icontains)
                - document_number: Búsqueda exacta
        
        Returns:
            Tupla: (lista_de_afiliados, total_count)
        """
        # Construir query base
        queryset = AffiliateORM.objects.all()
        
        # Aplicar filtros si existen
        if filters:
            # Filtro por status
            if 'status' in filters and filters['status']:
                queryset = queryset.filter(status=filters['status'])
            
            # Filtro por nombre (búsqueda parcial, case-insensitive)
            if 'full_name' in filters and filters['full_name']:
                queryset = queryset.filter(
                    full_name__icontains=filters['full_name']
                )
            
            # Filtro por documento (búsqueda exacta)
            if 'document_number' in filters and filters['document_number']:
                queryset = queryset.filter(
                    document_number=filters['document_number']
                )
        
        # Total de registros (antes de paginar)
        total_count = queryset.count()
        
        # Aplicar paginación
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Convertir ORM models a entidades de dominio
        affiliates = [self._to_domain(orm) for orm in page_obj.object_list]
        
        return affiliates, total_count
    
    def delete(self, affiliate_id: int) -> None:
        """
        Elimina un afiliado de la base de datos
        
        Django eliminará automáticamente las contribuciones relacionadas
        por la relación CASCADE definida en el modelo.
        """
        AffiliateORM.objects.filter(pk=affiliate_id).delete()
    
    # =========================================================================
    # Métodos privados de traducción (mappers)
    # =========================================================================
    
    def _to_domain(self, orm_model: AffiliateORM) -> Affiliate:
        """
        Convierte: AffiliateORM (Django) → Affiliate (Dominio)
        
        Este método "traduce" del lenguaje de la base de datos
        al lenguaje del negocio.
        """
        return Affiliate(
            id=orm_model.id,
            full_name=orm_model.full_name,
            document_type=DocumentType(orm_model.document_type),
            document_number=orm_model.document_number,
            email=Email(orm_model.email),
            status=AffiliateStatus(orm_model.status),
            phone_number=orm_model.phone_number,
            address=orm_model.address,
            notes=orm_model.notes,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )
    
    def _to_orm(
        self,
        affiliate: Affiliate,
        orm_model: Optional[AffiliateORM] = None
    ) -> AffiliateORM:
        """
        Convierte: Affiliate (Dominio) → AffiliateORM (Django)
        
        Este método "traduce" del lenguaje del negocio
        al lenguaje de la base de datos.
        
        Args:
            affiliate: Entidad de dominio
            orm_model: Instancia ORM existente (para updates) o None (para creates)
        """
        if orm_model is None:
            orm_model = AffiliateORM()
        
        # Mapear campos simples
        orm_model.full_name = affiliate.full_name
        orm_model.document_type = affiliate.document_type.value
        orm_model.document_number = affiliate.document_number
        orm_model.email = affiliate.email.value
        orm_model.status = affiliate.status.value
        orm_model.phone_number = affiliate.phone_number
        orm_model.address = affiliate.address
        orm_model.notes = affiliate.notes
        
        # Los timestamps los maneja Django automáticamente
        # pero los sincronizamos por consistencia
        if affiliate.created_at:
            orm_model.created_at = affiliate.created_at
        if affiliate.updated_at:
            orm_model.updated_at = affiliate.updated_at
        
        return orm_model

