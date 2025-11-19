"""Domain Models"""
from .value_objects import (
    Email,
    DocumentType,
    AffiliateStatus,
    PaymentMethod,
    Money
)
from .affiliate import Affiliate
from .contribution import Contribution

__all__ = [
    'Email',
    'DocumentType',
    'AffiliateStatus',
    'PaymentMethod',
    'Money',
    'Affiliate',
    'Contribution',
]

