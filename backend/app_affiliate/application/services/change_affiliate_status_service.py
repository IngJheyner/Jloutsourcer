"""
Use Case: Change Affiliate Status

Caso de uso para cambiar el estado de un afiliado (ACTIVE/INACTIVE).
"""
from ...domain.models import Affiliate, AffiliateStatus
from ...domain.interfaces import IAffiliateRepository
from ...domain.exceptions import AffiliateNotFoundError


class ChangeAffiliateStatusService:
    """Caso de uso: Cambiar Estado del Afiliado"""
    
    def __init__(self, affiliate_repository: IAffiliateRepository):
        self.affiliate_repository = affiliate_repository
    
    def execute(self, affiliate_id: int, new_status: str) -> Affiliate:
        """
        Cambia el estado de un afiliado
        
        Args:
            affiliate_id: ID del afiliado
            new_status: Nuevo estado ('ACTIVE' o 'INACTIVE')
        
        Returns:
            Affiliate con el nuevo estado
            
        Raises:
            AffiliateNotFoundError: Si el afiliado no existe
            AffiliateAlreadyActiveError: Si ya está activo
            AffiliateAlreadyInactiveError: Si ya está inactivo
        """
        # Buscar afiliado
        affiliate = self.affiliate_repository.find_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(str(affiliate_id))
        
        # Cambiar estado usando métodos del dominio
        status = AffiliateStatus(new_status)
        
        if status == AffiliateStatus.ACTIVE:
            affiliate.activate()  # Lógica de negocio en el dominio
        else:
            affiliate.deactivate()
        
        # Persistir cambios
        return self.affiliate_repository.save(affiliate)

