"""
Domain Exceptions

Excepciones específicas del dominio de negocio.
Independientes de la infraestructura (Django, HTTP, etc.)
"""


class DomainException(Exception):
    """Excepción base para el dominio"""
    pass


# Affiliate Exceptions
class AffiliateAlreadyExistsError(DomainException):
    """El afiliado ya existe en el sistema"""
    def __init__(self, document_number: str):
        self.document_number = document_number
        super().__init__(f"Affiliate with document {document_number} already exists")


class AffiliateNotFoundError(DomainException):
    """El afiliado no fue encontrado"""
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Affiliate {identifier} not found")


class InvalidAffiliateNameError(DomainException):
    """Nombre de afiliado inválido"""
    pass


class InvalidDocumentError(DomainException):
    """Documento inválido"""
    pass


class AffiliateAlreadyActiveError(DomainException):
    """El afiliado ya está activo"""
    def __init__(self):
        super().__init__("Affiliate is already active")


class AffiliateAlreadyInactiveError(DomainException):
    """El afiliado ya está inactivo"""
    def __init__(self):
        super().__init__("Affiliate is already inactive")


# Contribution Exceptions
class ContributionNotFoundError(DomainException):
    """El aporte no fue encontrado"""
    def __init__(self, contribution_id: int):
        self.contribution_id = contribution_id
        super().__init__(f"Contribution {contribution_id} not found")


class InvalidAmountError(DomainException):
    """Monto inválido"""
    pass


class InvalidContributionDateError(DomainException):
    """Fecha de aporte inválida"""
    pass


# Value Object Exceptions
class InvalidEmailError(DomainException):
    """Email inválido"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' is not valid")


class InvalidPaymentMethodError(DomainException):
    """Método de pago inválido"""
    pass

