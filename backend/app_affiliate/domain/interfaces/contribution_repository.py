"""
Repository Interface: Contribution

Define el contrato para el repositorio de aportes.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from datetime import date
from ..models.contribution import Contribution


class IContributionRepository(ABC):
    """
    Interfaz del repositorio de aportes
    
    Define las operaciones necesarias para gestionar aportes.
    """
    
    @abstractmethod
    def save(self, contribution: Contribution) -> Contribution:
        """
        Guarda o actualiza un aporte
        
        Args:
            contribution: Entidad de aporte a guardar
            
        Returns:
            Aporte guardado con ID asignado
        """
        pass
    
    @abstractmethod
    def find_by_id(self, contribution_id: int) -> Optional[Contribution]:
        """
        Busca un aporte por su ID
        
        Args:
            contribution_id: ID del aporte
            
        Returns:
            Aporte si existe, None si no
        """
        pass
    
    @abstractmethod
    def find_by_affiliate(
        self,
        affiliate_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> tuple[List[Contribution], int]:
        """
        Lista aportes de un afiliado específico
        
        Args:
            affiliate_id: ID del afiliado
            page: Número de página
            page_size: Elementos por página
            
        Returns:
            Tupla con (lista_de_aportes, total_count)
        """
        pass
    
    @abstractmethod
    def get_summary(self, affiliate_id: int) -> dict:
        """
        Obtiene resumen estadístico de aportes de un afiliado
        
        Args:
            affiliate_id: ID del afiliado
            
        Returns:
            Diccionario con:
            - total_amount: Suma total de aportes
            - count: Cantidad de aportes
            - last_contribution_date: Fecha del último aporte
        """
        pass
    
    @abstractmethod
    def delete(self, contribution_id: int) -> None:
        """
        Elimina un aporte
        
        Args:
            contribution_id: ID del aporte a eliminar
        """
        pass

