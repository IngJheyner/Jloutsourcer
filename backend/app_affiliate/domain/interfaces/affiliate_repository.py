"""
Repository Interface: Affiliate

Define el contrato (interfaz) que debe cumplir cualquier implementación
del repositorio de afiliados. Esto es Dependency Inversion (SOLID).
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.affiliate import Affiliate


class IAffiliateRepository(ABC):
    """
    Interfaz del repositorio de afiliados
    
    Define QUÉ operaciones necesita el dominio, sin especificar CÓMO se implementan.
    La capa de infraestructura será responsable de la implementación concreta.
    """
    
    @abstractmethod
    def save(self, affiliate: Affiliate) -> Affiliate:
        """
        Guarda o actualiza un afiliado
        
        Args:
            affiliate: Entidad de afiliado a guardar
            
        Returns:
            Afiliado guardado con ID asignado
        """
        pass
    
    @abstractmethod
    def find_by_id(self, affiliate_id: int) -> Optional[Affiliate]:
        """
        Busca un afiliado por su ID
        
        Args:
            affiliate_id: ID del afiliado
            
        Returns:
            Afiliado si existe, None si no
        """
        pass
    
    @abstractmethod
    def find_by_document(self, document_number: str) -> Optional[Affiliate]:
        """
        Busca un afiliado por número de documento
        
        Args:
            document_number: Número de documento único
            
        Returns:
            Afiliado si existe, None si no
        """
        pass
    
    @abstractmethod
    def exists_by_document(self, document_number: str) -> bool:
        """
        Verifica si existe un afiliado con el documento dado
        
        Args:
            document_number: Número de documento
            
        Returns:
            True si existe, False si no
        """
        pass
    
    @abstractmethod
    def list_all(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[dict] = None
    ) -> tuple[List[Affiliate], int]:
        """
        Lista afiliados con paginación y filtros opcionales
        
        Args:
            page: Número de página (base 1)
            page_size: Cantidad de elementos por página
            filters: Filtros opcionales (status, full_name, etc.)
            
        Returns:
            Tupla con (lista_de_afiliados, total_count)
        """
        pass
    
    @abstractmethod
    def delete(self, affiliate_id: int) -> None:
        """
        Elimina un afiliado
        
        Args:
            affiliate_id: ID del afiliado a eliminar
        """
        pass

