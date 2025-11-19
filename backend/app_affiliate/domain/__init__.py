"""Domain Layer - Core Business Logic"""
from .models import (
    Email,
    DocumentType,
    AffiliateStatus,
    PaymentMethod,
    Money,
    Affiliate,
    Contribution,
)
from .interfaces import (
    IAffiliateRepository,
    IContributionRepository,
)
from .exceptions import (
    DomainException,
    AffiliateAlreadyExistsError,
    AffiliateNotFoundError,
    ContributionNotFoundError,
    InvalidEmailError,
    InvalidAmountError,
)

__all__ = [
    # Value Objects
    'Email',
    'DocumentType',
    'AffiliateStatus',
    'PaymentMethod',
    'Money',
    # Entities
    'Affiliate',
    'Contribution',
    # Interfaces
    'IAffiliateRepository',
    'IContributionRepository',
    # Exceptions
    'DomainException',
    'AffiliateAlreadyExistsError',
    'AffiliateNotFoundError',
    'ContributionNotFoundError',
    'InvalidEmailError',
    'InvalidAmountError',
]

