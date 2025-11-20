"""
Use Case: Register Contribution

Caso de uso para registrar un nuevo aporte de un afiliado.
"""
from datetime import date

from ...domain.models import Contribution, Money, PaymentMethod
from ...domain.interfaces import IAffiliateRepository, IContributionRepository
from ...domain.exceptions import AffiliateNotFoundError


class RegisterContributionService:
    """Caso de uso: Registrar Aporte"""
    
    def __init__(
        self,
        affiliate_repository: IAffiliateRepository,
        contribution_repository: IContributionRepository
    ):
        self.affiliate_repository = affiliate_repository
        self.contribution_repository = contribution_repository
    
    def execute(self, affiliate_id: int, data: dict) -> Contribution:
        """
        Registra un nuevo aporte
        
        Args:
            affiliate_id: ID del afiliado que realiza el aporte
            data: Datos del aporte:
                {
                    'amount': float,
                    'contribution_date': str (YYYY-MM-DD),
                    'payment_method': str,  # 'CASH', 'TRANSFER', 'CARD'
                    'reference_number': str (opcional),
                    'notes': str (opcional)
                }
        
        Returns:
            Contribution creado
            
        Raises:
            AffiliateNotFoundError: Si el afiliado no existe
            InvalidAmountError: Si el monto es inválido
            InvalidContributionDateError: Si la fecha es inválida
        """
        # Verificar que el afiliado existe
        affiliate = self.affiliate_repository.find_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(str(affiliate_id))
        
        # Crear Value Objects
        amount = Money(data['amount'])
        payment_method = PaymentMethod.from_string(data['payment_method'])
        
        # Parsear fecha
        if isinstance(data['contribution_date'], str):
            contribution_date = date.fromisoformat(data['contribution_date'])
        else:
            contribution_date = data['contribution_date']
        
        # Crear entidad de dominio (con validaciones)
        contribution = Contribution.create(
            affiliate_id=affiliate_id,
            amount=amount,
            contribution_date=contribution_date,
            payment_method=payment_method,
            reference_number=data.get('reference_number'),
            notes=data.get('notes')
        )
        
        # Persistir
        return self.contribution_repository.save(contribution)

