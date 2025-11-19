"""
Entity: Affiliate

Entidad de dominio que representa un afiliado de la cooperativa.
Contiene lógica de negocio pura, independiente de la infraestructura.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .value_objects import Email, DocumentType, AffiliateStatus
from ..exceptions import (
    InvalidAffiliateNameError,
    InvalidDocumentError,
    AffiliateAlreadyActiveError,
    AffiliateAlreadyInactiveError
)


@dataclass
class Affiliate:
    """
    Entidad: Afiliado
    
    Representa un miembro de la cooperativa con su información
    y comportamientos asociados.
    """
    
    id: Optional[int]
    full_name: str
    document_type: DocumentType
    document_number: str
    email: Email
    status: AffiliateStatus
    created_at: datetime
    updated_at: datetime
    
    # Campos opcionales
    phone_number: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    
    @staticmethod
    def create(
        full_name: str,
        document_type: DocumentType,
        document_number: str,
        email: Email,
        status: Optional[AffiliateStatus] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None
    ) -> 'Affiliate':
        """
        Factory method: Crea un nuevo afiliado con validaciones de negocio
        
        Args:
            full_name: Nombre completo del afiliado
            document_type: Tipo de documento (CC, CE, NIT)
            document_number: Número de documento único
            email: Email validado
            status: Estado inicial (por defecto ACTIVE)
            phone_number: Teléfono opcional
            address: Dirección opcional
            notes: Notas opcionales
            
        Returns:
            Nueva instancia de Affiliate
            
        Raises:
            InvalidAffiliateNameError: Si el nombre es inválido
            InvalidDocumentError: Si el documento es inválido
        """
        # Validar nombre
        full_name = full_name.strip()
        if len(full_name) < 3:
            raise InvalidAffiliateNameError(
                "Full name must be at least 3 characters"
            )
        
        # Validar documento
        document_number = document_number.strip()
        if not document_number:
            raise InvalidDocumentError(
                "Document number cannot be empty"
            )
        
        # Validaciones por tipo de documento
        if document_type == DocumentType.NIT:
            if len(document_number.replace('-', '')) < 9:
                raise InvalidDocumentError(
                    "NIT must have at least 9 digits"
                )
        elif document_type in [DocumentType.CC, DocumentType.CE]:
            if not document_number.replace('-', '').isdigit():
                raise InvalidDocumentError(
                    f"Document type {document_type.value} must be numeric"
                )
        
        # Estado por defecto
        if status is None:
            status = AffiliateStatus.ACTIVE
        
        now = datetime.now()
        
        return Affiliate(
            id=None,
            full_name=full_name,
            document_type=document_type,
            document_number=document_number,
            email=email,
            status=status,
            phone_number=phone_number,
            address=address,
            notes=notes,
            created_at=now,
            updated_at=now
        )
    
    def activate(self) -> None:
        """
        Activa el afiliado
        
        Regla de negocio: Solo se puede activar si está inactivo
        
        Raises:
            AffiliateAlreadyActiveError: Si ya está activo
        """
        if self.status == AffiliateStatus.ACTIVE:
            raise AffiliateAlreadyActiveError()
        
        self.status = AffiliateStatus.ACTIVE
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """
        Desactiva el afiliado
        
        Regla de negocio: Solo se puede desactivar si está activo
        
        Raises:
            AffiliateAlreadyInactiveError: Si ya está inactivo
        """
        if self.status == AffiliateStatus.INACTIVE:
            raise AffiliateAlreadyInactiveError()
        
        self.status = AffiliateStatus.INACTIVE
        self.updated_at = datetime.now()
    
    def update_contact_info(
        self,
        email: Optional[Email] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None
    ) -> None:
        """Actualiza información de contacto"""
        if email is not None:
            self.email = email
        if phone_number is not None:
            self.phone_number = phone_number
        if address is not None:
            self.address = address
        
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """Verifica si el afiliado está activo"""
        return self.status == AffiliateStatus.ACTIVE
    
    def is_inactive(self) -> bool:
        """Verifica si el afiliado está inactivo"""
        return self.status == AffiliateStatus.INACTIVE
    
    def __str__(self) -> str:
        return f"Affiliate({self.full_name} - {self.document_number})"
    
    def __repr__(self) -> str:
        return (
            f"Affiliate(id={self.id}, full_name='{self.full_name}', "
            f"document_number='{self.document_number}', status={self.status})"
        )

