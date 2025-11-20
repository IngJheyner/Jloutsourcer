"""
Use Case: Create Affiliate

Caso de uso para crear un nuevo afiliado en el sistema.
Orquesta las validaciones del dominio y la persistencia en infraestructura.
"""
from ...domain.models import Affiliate, Email, DocumentType, AffiliateStatus
from ...domain.interfaces import IAffiliateRepository
from ...domain.exceptions import AffiliateAlreadyExistsError


class CreateAffiliateService:
    """
    Caso de uso: Crear Afiliado
    
    Responsabilidades:
    1. Verificar que no exista un afiliado con el mismo documento
    2. Crear la entidad de dominio (con validaciones)
    3. Persistir usando el repositorio
    """
    
    def __init__(self, affiliate_repository: IAffiliateRepository):
        """
        Inyección de dependencias
        
        Args:
            affiliate_repository: Implementación del repositorio
                                 (puede ser DjangoAffiliateRepository u otra)
        """
        self.affiliate_repository = affiliate_repository
    
    def execute(self, data: dict) -> Affiliate:
        """
        Ejecuta el caso de uso
        
        Args:
            data: Diccionario con los datos del afiliado:
                {
                    'full_name': str,
                    'document_type': str,  # 'CC', 'CE', 'NIT'
                    'document_number': str,
                    'email': str,
                    'status': str (opcional),  # 'ACTIVE', 'INACTIVE'
                    'phone_number': str (opcional),
                    'address': str (opcional),
                    'notes': str (opcional)
                }
        
        Returns:
            Affiliate creado con ID asignado
            
        Raises:
            AffiliateAlreadyExistsError: Si ya existe con ese documento
            InvalidEmailError: Si el email es inválido
            InvalidAffiliateNameError: Si el nombre es inválido
        """
        # Paso 1: Verificar que no exista (regla de negocio)
        if self.affiliate_repository.exists_by_document(data['document_number']):
            raise AffiliateAlreadyExistsError(data['document_number'])
        
        # Paso 2: Crear Value Objects
        email = Email(data['email'])
        document_type = DocumentType.from_string(data['document_type'])
        
        # Status opcional (por defecto ACTIVE)
        status = None
        if 'status' in data and data['status']:
            status = AffiliateStatus(data['status'])
        
        # Paso 3: Crear entidad de dominio (con validaciones)
        affiliate = Affiliate.create(
            full_name=data['full_name'],
            document_type=document_type,
            document_number=data['document_number'],
            email=email,
            status=status,
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            notes=data.get('notes')
        )
        
        # Paso 4: Persistir usando el repositorio
        return self.affiliate_repository.save(affiliate)

