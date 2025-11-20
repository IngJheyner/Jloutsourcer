"""
Use Case: Get Affiliate Summary

Caso de uso para obtener el resumen estadístico de aportes de un afiliado.
"""
from ...domain.interfaces import IAffiliateRepository, IContributionRepository
from ...domain.exceptions import AffiliateNotFoundError


class GetAffiliateSummaryService:
    """Caso de uso: Obtener Resumen de Afiliado"""
    
    def __init__(
        self,
        affiliate_repository: IAffiliateRepository,
        contribution_repository: IContributionRepository
    ):
        self.affiliate_repository = affiliate_repository
        self.contribution_repository = contribution_repository
    
    def execute(self, affiliate_id: int) -> dict:
        """
        Obtiene el resumen de aportes de un afiliado
        
        Args:
            affiliate_id: ID del afiliado
        
        Returns:
            {
                'affiliate': {
                    'full_name': str,
                    'document_number': str,
                    'status': str
                },
                'total_contributions': float,
                'contributions_count': int,
                'last_contribution_date': str (YYYY-MM-DD) o None
            }
            
        Raises:
            AffiliateNotFoundError: Si el afiliado no existe
        """
        # Buscar afiliado
        affiliate = self.affiliate_repository.find_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(str(affiliate_id))
        
        # Obtener estadísticas de aportes
        summary = self.contribution_repository.get_summary(affiliate_id)
        
        # Formatear respuesta
        return {
            'affiliate': {
                'full_name': affiliate.full_name,
                'document_number': affiliate.document_number,
                'status': affiliate.status.value
            },
            'total_contributions': float(summary['total_amount']),
            'contributions_count': summary['count'],
            'last_contribution_date': (
                summary['last_contribution_date'].isoformat()
                if summary['last_contribution_date']
                else None
            )
        }

