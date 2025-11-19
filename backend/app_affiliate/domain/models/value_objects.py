"""
Value Objects

Objetos inmutables que representan conceptos del dominio.
Se identifican por su valor, no por su identidad.
"""
from enum import Enum
from decimal import Decimal
from typing import Any
import re

from ..exceptions import (
    InvalidEmailError,
    InvalidAmountError,
    InvalidDocumentError,
    InvalidPaymentMethodError
)


class Email:
    """Value Object: Email validado"""
    
    _EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise InvalidEmailError(value)
        self._value = value.lower().strip()
    
    @staticmethod
    def _is_valid(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False
        return re.match(Email._EMAIL_PATTERN, email) is not None
    
    @property
    def value(self) -> str:
        return self._value
    
    def __str__(self) -> str:
        return self._value
    
    def __repr__(self) -> str:
        return f"Email('{self._value}')"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Email):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)


class DocumentType(str, Enum):
    """Value Object: Tipo de documento"""
    CC = "CC"    # Cédula de Ciudadanía
    CE = "CE"    # Cédula de Extranjería
    NIT = "NIT"  # Número de Identificación Tributaria
    
    @classmethod
    def from_string(cls, value: str) -> 'DocumentType':
        try:
            return cls[value.upper()]
        except KeyError:
            raise InvalidDocumentError(
                f"Document type '{value}' invalid. Options: CC, CE, NIT"
            )


class AffiliateStatus(str, Enum):
    """Value Object: Estado del afiliado"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    
    def is_active(self) -> bool:
        return self == AffiliateStatus.ACTIVE
    
    def is_inactive(self) -> bool:
        return self == AffiliateStatus.INACTIVE


class PaymentMethod(str, Enum):
    """Value Object: Método de pago"""
    CASH = "CASH"          # Efectivo
    TRANSFER = "TRANSFER"  # Transferencia bancaria
    CARD = "CARD"          # Tarjeta de crédito/débito
    
    @classmethod
    def from_string(cls, value: str) -> 'PaymentMethod':
        try:
            return cls[value.upper()]
        except KeyError:
            raise InvalidPaymentMethodError(
                f"Payment method '{value}' invalid. Options: CASH, TRANSFER, CARD"
            )


class Money:
    """Value Object: Dinero con validación"""
    
    def __init__(self, amount: float | Decimal | int):
        if isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        if not isinstance(amount, Decimal):
            raise InvalidAmountError(
                f"Amount must be a number, received: {type(amount)}"
            )
        
        if amount < 0:
            raise InvalidAmountError(
                f"Amount cannot be negative: {amount}"
            )
        
        # Redondear a 2 decimales para precisión monetaria
        self._amount = amount.quantize(Decimal('0.01'))
    
    @property
    def amount(self) -> Decimal:
        return self._amount
    
    @property
    def as_float(self) -> float:
        return float(self._amount)
    
    def __str__(self) -> str:
        return f"{self._amount:.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self._amount})"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self._amount == other._amount
    
    def __lt__(self, other: 'Money') -> bool:
        return self._amount < other._amount
    
    def __le__(self, other: 'Money') -> bool:
        return self._amount <= other._amount
    
    def __gt__(self, other: 'Money') -> bool:
        return self._amount > other._amount
    
    def __ge__(self, other: 'Money') -> bool:
        return self._amount >= other._amount
    
    def __add__(self, other: 'Money') -> 'Money':
        return Money(self._amount + other._amount)
    
    def __sub__(self, other: 'Money') -> 'Money':
        result = self._amount - other._amount
        if result < 0:
            raise InvalidAmountError("Subtraction results in negative amount")
        return Money(result)
    
    def __hash__(self) -> int:
        return hash(self._amount)
    
    @staticmethod
    def zero() -> 'Money':
        return Money(Decimal('0.00'))

