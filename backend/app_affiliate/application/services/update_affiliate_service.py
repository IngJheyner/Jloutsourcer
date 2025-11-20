"""
Use Case: Update Affiliate

Caso de uso para actualizar un afiliado existente.
"""
from typing import Optional

from ...domain.models import Affiliate, Email
from ...domain.interfaces import IAffiliateRepository
from ...domain.exceptions import AffiliateNotFoundError


class UpdateAffiliateService:
    """Caso de uso: Actualizar Afiliado"""
    
    def __init__(self, affiliate_repository: IAffiliateRepository):
        self.affiliate_repository = affiliate_repository
    
    def execute(self, affiliate_id: int, data: dict) -> Affiliate:
        """
        Actualiza un afiliado existente
        
        Args:
            affiliate_id: ID del afiliado a actualizar
            data: Datos a actualizar (solo los campos presentes)
        
        Returns:
            Affiliate actualizado
            
        Raises:
            AffiliateNotFoundError: Si el afiliado no existe
        """
        # Buscar afiliado existente
        affiliate = self.affiliate_repository.find_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(str(affiliate_id))
        
        # Actualizar campos si están presentes
        if 'full_name' in data:
            affiliate.full_name = data['full_name'].strip()
        
        if 'email' in data:
            affiliate.email = Email(data['email'])
        
        if 'phone_number' in data:
            affiliate.phone_number = data['phone_number']
        
        if 'address' in data:
            affiliate.address = data['address']
        
        if 'notes' in data:
            affiliate.notes = data['notes']
        
        # Guardar cambios
        return self.affiliate_repository.save(affiliate)

