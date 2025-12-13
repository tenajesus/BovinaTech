"""
Modelo Animal con propiedades calculadas de edad y categoría.
Desarrollado siguiendo buenas prácticas de Python con Type Hints.
"""

from datetime import date, datetime
from typing import Optional, Dict, Any


class Animal:
    """
    Representa un animal en el sistema ganadero.
    
    Attributes:
        id_animal (int): Identificador único del animal
        arete (str): Número de arete/identificación
        origen (str): 'nacido' o 'comprado'
        peso_inicial (float): Peso inicial en kg
        fecha_ingreso (date): Fecha de ingreso al rancho
        fecha_nacimiento (date): Fecha de nacimiento del animal
        raza (str): Raza del animal
        sexo (str): 'Macho' o 'Hembra'
        observaciones (str): Notas adicionales
        id_lote (int): ID del lote al que pertenece
        id_proveedor (int): ID del proveedor (si fue comprado)
    """
    
    def __init__(
        self,
        id_animal: int,
        arete: str,
        origen: str,
        fecha_nacimiento: Optional[date] = None,
        fecha_ingreso: Optional[date] = None,
        peso_inicial: Optional[float] = None,
        raza: Optional[str] = None,
        sexo: Optional[str] = None,
        observaciones: Optional[str] = None,
        id_lote: Optional[int] = None,
        id_proveedor: Optional[int] = None
    ):
        self.id_animal = id_animal
        self.arete = arete
        self.origen = origen
        self.peso_inicial = peso_inicial
        self.fecha_ingreso = fecha_ingreso
        self.fecha_nacimiento = fecha_nacimiento
        self.raza = raza
        self.sexo = sexo
        self.observaciones = observaciones
        self.id_lote = id_lote
        self.id_proveedor = id_proveedor
    
    def edad_en_dias(self) -> int:
        """
        Calcula la edad del animal en días desde su nacimiento.
        
        Returns:
            int: Edad en días. Retorna 0 si no hay fecha de nacimiento.
        
        Example:
            >>> animal = Animal(1, 'A001', 'nacido', fecha_nacimiento=date(2024, 1, 1))
            >>> animal.edad_en_dias()  # Si hoy es 2024-03-01
            60
        """
        if not self.fecha_nacimiento:
            return 0
        
        hoy = date.today()
        delta = hoy - self.fecha_nacimiento
        return delta.days
    
    def edad_en_meses(self) -> int:
        """
        Calcula la edad del animal en meses (aproximado).
        
        Returns:
            int: Edad en meses (días / 30)
        """
        return self.edad_en_dias() // 30
    
    def categoria_edad(self) -> str:
        """
        Determina la categoría del animal según su edad.
        
        Categorías veterinarias:
        - Cría: 0-6 meses (0-180 días)
        - Destete: 6-8 meses (180-240 días)
        - Desarrollo: 8-18 meses (240-540 días)
        - Adulto: >18 meses (>540 días)
        
        Returns:
            str: Categoría del animal
        """
        dias = self.edad_en_dias()
        
        if dias < 180:
            return 'Cría'
        elif dias < 240:
            return 'Destete'
        elif dias < 540:
            return 'Desarrollo'
        else:
            return 'Adulto'
    
    def es_hembra(self) -> bool:
        """
        Verifica si el animal es hembra.
        
        Returns:
            bool: True si es hembra, False en caso contrario
        """
        return self.sexo == 'Hembra'
    
    def es_macho(self) -> bool:
        """
        Verifica si el animal es macho.
        
        Returns:
            bool: True si es macho, False en caso contrario
        """
        return self.sexo == 'Macho'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Animal a un diccionario para serialización.
        
        Returns:
            Dict: Representación en diccionario del animal
        """
        return {
            'id_animal': self.id_animal,
            'arete': self.arete,
            'origen': self.origen,
            'peso_inicial': float(self.peso_inicial) if self.peso_inicial else None,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'raza': self.raza,
            'sexo': self.sexo,
            'observaciones': self.observaciones,
            'id_lote': self.id_lote,
            'id_proveedor': self.id_proveedor,
            'edad_dias': self.edad_en_dias(),
            'edad_meses': self.edad_en_meses(),
            'categoria_edad': self.categoria_edad()
        }
    
    @staticmethod
    def from_db_row(row: Dict[str, Any]) -> 'Animal':
        """
        Crea una instancia de Animal desde un registro de base de datos.
        
        Args:
            row (Dict): Diccionario con los datos del animal desde la BD
        
        Returns:
            Animal: Instancia del animal
        """
        # Convertir fechas si vienen como string
        fecha_nacimiento = row.get('fecha_nacimiento')
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        
        fecha_ingreso = row.get('fecha_ingreso')
        if isinstance(fecha_ingreso, str):
            fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
        
        return Animal(
            id_animal=row['id_animal'],
            arete=row['arete'],
            origen=row['origen'],
            fecha_nacimiento=fecha_nacimiento,
            fecha_ingreso=fecha_ingreso,
            peso_inicial=row.get('peso_inicial'),
            raza=row.get('raza'),
            sexo=row.get('sexo'),
            observaciones=row.get('observaciones'),
            id_lote=row.get('id_lote'),
            id_proveedor=row.get('id_proveedor')
        )
    
    def __repr__(self) -> str:
        """Representación en string del animal."""
        return f"Animal(arete='{self.arete}', edad={self.edad_en_meses()}m, categoria='{self.categoria_edad()}')"
