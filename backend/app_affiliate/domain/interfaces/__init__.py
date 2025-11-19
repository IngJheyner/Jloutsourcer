"""Domain Interfaces (Repositories)"""
from .affiliate_repository import IAffiliateRepository
from .contribution_repository import IContributionRepository

__all__ = [
    'IAffiliateRepository',
    'IContributionRepository',
]

