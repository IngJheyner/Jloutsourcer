"""
Entity: Contribution

Entidad de dominio que representa un aporte de un afiliado.
Contiene lógica de negocio pura, independiente de la infraestructura.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from .value_objects import Money, PaymentMethod
from ..exceptions import InvalidAmountError, InvalidContributionDateError


@dataclass
class Contribution:
    """
    Entidad: Aporte
    
    Representa un aporte monetario realizado por un afiliado
    en una fecha específica.
    """
    
    id: Optional[int]
    affiliate_id: int
    amount: Money
    contribution_date: date
    payment_method: PaymentMethod
    created_at: datetime
    updated_at: datetime
    
    # Campos opcionales
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    verified: bool = False
    
    @staticmethod
    def create(
        affiliate_id: int,
        amount: Money,
        contribution_date: date,
        payment_method: PaymentMethod,
        reference_number: Optional[str] = None,
        notes: Optional[str] = None,
        verified: bool = False
    ) -> 'Contribution':
        """
        Factory method: Crea un nuevo aporte con validaciones de negocio
        
        Args:
            affiliate_id: ID del afiliado que realiza el aporte
            amount: Monto del aporte
            contribution_date: Fecha en que se realizó el aporte
            payment_method: Método de pago utilizado
            reference_number: Número de referencia opcional
            notes: Notas opcionales
            verified: Si el aporte fue verificado
            
        Returns:
            Nueva instancia de Contribution
            
        Raises:
            InvalidAmountError: Si el monto es inválido
            InvalidContributionDateError: Si la fecha es inválida
        """
        # Validar monto
        if amount.amount <= 0:
            raise InvalidAmountError(
                "Contribution amount must be greater than zero"
            )
        
        # Validar fecha (no puede ser futura)
        today = date.today()
        if contribution_date > today:
            raise InvalidContributionDateError(
                f"Contribution date cannot be in the future. "
                f"Received: {contribution_date}, Today: {today}"
            )
        
        # Validar affiliate_id
        if affiliate_id <= 0:
            raise ValueError("Affiliate ID must be a positive number")
        
        now = datetime.now()
        
        return Contribution(
            id=None,
            affiliate_id=affiliate_id,
            amount=amount,
            contribution_date=contribution_date,
            payment_method=payment_method,
            reference_number=reference_number,
            notes=notes,
            verified=verified,
            created_at=now,
            updated_at=now
        )
    
    def verify(self) -> None:
        """Marca el aporte como verificado"""
        self.verified = True
        self.updated_at = datetime.now()
    
    def unverify(self) -> None:
        """Marca el aporte como no verificado"""
        self.verified = False
        self.updated_at = datetime.now()
    
    def update_amount(self, new_amount: Money) -> None:
        """
        Actualiza el monto del aporte
        
        Args:
            new_amount: Nuevo monto
            
        Raises:
            InvalidAmountError: Si el nuevo monto es inválido
        """
        if new_amount.amount <= 0:
            raise InvalidAmountError(
                "Contribution amount must be greater than zero"
            )
        
        self.amount = new_amount
        self.updated_at = datetime.now()
    
    def is_verified(self) -> bool:
        """Verifica si el aporte ha sido verificado"""
        return self.verified
    
    def is_recent(self, days: int = 30) -> bool:
        """
        Verifica si el aporte es reciente
        
        Args:
            days: Número de días para considerar "reciente"
            
        Returns:
            True si el aporte es de los últimos N días
        """
        today = date.today()
        delta = today - self.contribution_date
        return delta.days <= days
    
    def __str__(self) -> str:
        return (
            f"Contribution(affiliate_id={self.affiliate_id}, "
            f"amount={self.amount}, date={self.contribution_date})"
        )
    
    def __repr__(self) -> str:
        return (
            f"Contribution(id={self.id}, affiliate_id={self.affiliate_id}, "
            f"amount={self.amount}, contribution_date={self.contribution_date}, "
            f"payment_method={self.payment_method})"
        )

