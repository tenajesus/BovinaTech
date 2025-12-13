"""
Servicios de negocio para el sistema de gestión ganadera.
"""

from .vacunacion_service import VacunacionService
from .desparasitacion_service import DesparasitacionService

__all__ = ['VacunacionService', 'DesparasitacionService']
