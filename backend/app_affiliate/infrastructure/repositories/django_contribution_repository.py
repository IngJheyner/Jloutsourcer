"""
Django Contribution Repository

Implementación concreta del repositorio de aportes usando Django ORM.
"""
from typing import List, Optional
from decimal import Decimal
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Max

from ...domain.interfaces import IContributionRepository
from ...domain.models import Contribution, Money, PaymentMethod
from .orm_models import ContributionORM


class DjangoContributionRepository(IContributionRepository):
    """
    Repositorio de aportes usando Django ORM
    
    Implementa la interfaz IContributionRepository definida en el dominio.
    """
    
    def save(self, contribution: Contribution) -> Contribution:
        """Guarda o actualiza un aporte"""
        if contribution.id:
            try:
                orm_model = ContributionORM.objects.get(pk=contribution.id)
                orm_model = self._to_orm(contribution, orm_model)
            except ContributionORM.DoesNotExist:
                orm_model = self._to_orm(contribution)
        else:
            orm_model = self._to_orm(contribution)
        
        orm_model.save()
        return self._to_domain(orm_model)
    
    def find_by_id(self, contribution_id: int) -> Optional[Contribution]:
        """Busca un aporte por su ID"""
        try:
            orm_model = ContributionORM.objects.get(pk=contribution_id)
            return self._to_domain(orm_model)
        except ContributionORM.DoesNotExist:
            return None
    
    def find_by_affiliate(
        self,
        affiliate_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Contribution], int]:
        """
        Lista aportes de un afiliado específico
        
        Los aportes se ordenan por fecha DESC (más reciente primero)
        """
        # Query base: aportes del afiliado ordenados por fecha
        queryset = ContributionORM.objects.filter(
            affiliate_id=affiliate_id
        ).order_by('-contribution_date', '-created_at')
        
        # Total de registros
        total_count = queryset.count()
        
        # Paginar
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Convertir a entidades de dominio
        contributions = [self._to_domain(orm) for orm in page_obj.object_list]
        
        return contributions, total_count
    
    def get_summary(self, affiliate_id: int) -> dict:
        """
        Obtiene resumen estadístico de aportes de un afiliado
        
        Usa funciones de agregación de Django:
        - Sum: Suma total de montos
        - Count: Cantidad de aportes
        - Max: Fecha más reciente
        
        Returns:
            {
                'total_amount': Decimal('123456.78'),
                'count': 10,
                'last_contribution_date': date(2025, 11, 18)
            }
        """
        # Agregaciones en una sola query SQL (eficiente)
        summary = ContributionORM.objects.filter(
            affiliate_id=affiliate_id
        ).aggregate(
            total_amount=Sum('amount'),
            count=Count('id'),
            last_contribution_date=Max('contribution_date')
        )
        
        # Convertir None a valores por defecto
        return {
            'total_amount': summary['total_amount'] or Decimal('0.00'),
            'count': summary['count'] or 0,
            'last_contribution_date': summary['last_contribution_date']
        }
    
    def delete(self, contribution_id: int) -> None:
        """Elimina un aporte"""
        ContributionORM.objects.filter(pk=contribution_id).delete()
    
    # =========================================================================
    # Métodos privados de traducción (mappers)
    # =========================================================================
    
    def _to_domain(self, orm_model: ContributionORM) -> Contribution:
        """Convierte: ContributionORM → Contribution (dominio)"""
        return Contribution(
            id=orm_model.id,
            affiliate_id=orm_model.affiliate_id,
            amount=Money(orm_model.amount),
            contribution_date=orm_model.contribution_date,
            payment_method=PaymentMethod(orm_model.payment_method),
            reference_number=orm_model.reference_number,
            notes=orm_model.notes,
            verified=orm_model.verified,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )
    
    def _to_orm(
        self,
        contribution: Contribution,
        orm_model: Optional[ContributionORM] = None
    ) -> ContributionORM:
        """Convierte: Contribution (dominio) → ContributionORM"""
        if orm_model is None:
            orm_model = ContributionORM()
        
        orm_model.affiliate_id = contribution.affiliate_id
        orm_model.amount = contribution.amount.amount  # Decimal del Money
        orm_model.contribution_date = contribution.contribution_date
        orm_model.payment_method = contribution.payment_method.value
        orm_model.reference_number = contribution.reference_number
        orm_model.notes = contribution.notes
        orm_model.verified = contribution.verified
        
        if contribution.created_at:
            orm_model.created_at = contribution.created_at
        if contribution.updated_at:
            orm_model.updated_at = contribution.updated_at
        
        return orm_model

