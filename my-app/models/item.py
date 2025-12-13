"""
Modelo Item (medicamentos, alimentos, herramientas) con lógica de vacunas.
"""

from datetime import date, timedelta
from typing import Optional, Dict, Any


class Item:
    """
    Representa un item del inventario (medicamento, alimento, herramienta).
    
    Attributes:
        id_item (int): Identificador único
        nombre (str): Nombre del item
        tipo (str): 'medicamento', 'alimento', 'herramienta'
        costo (float): Costo unitario
        cantidad (float): Cantidad en inventario
        dias_retiro_carne (int): Días de retiro para carne
        dias_retiro_leche (int): Días de retiro para leche
        ingrediente_activo (str): Ingrediente activo (medicamentos)
        categoria_sanitaria (str): 'Vacuna', 'Desparasitante', 'Antibiotico', 'Vitamina', 'NA'
        unidad_medida (str): 'ml', 'dosis', 'gramos', 'unidad'
        requiere_refuerzo (bool): Si la vacuna requiere refuerzo
        dias_refuerzo (int): Días hasta el refuerzo
    """
    
    def __init__(
        self,
        id_item: int,
        nombre: str,
        tipo: str,
        costo: float,
        cantidad: float = 0.0,
        dias_retiro_carne: int = 0,
        dias_retiro_leche: int = 0,
        ingrediente_activo: Optional[str] = None,
        categoria_sanitaria: str = 'NA',
        unidad_medida: str = 'unidad',
        requiere_refuerzo: bool = False,
        dias_refuerzo: Optional[int] = None
    ):
        self.id_item = id_item
        self.nombre = nombre
        self.tipo = tipo
        self.costo = costo
        self.cantidad = cantidad
        self.dias_retiro_carne = dias_retiro_carne
        self.dias_retiro_leche = dias_retiro_leche
        self.ingrediente_activo = ingrediente_activo
        self.categoria_sanitaria = categoria_sanitaria
        self.unidad_medida = unidad_medida
        self.requiere_refuerzo = requiere_refuerzo
        self.dias_refuerzo = dias_refuerzo
    
    def es_vacuna(self) -> bool:
        """
        Verifica si el item es una vacuna.
        
        Returns:
            bool: True si es vacuna
        """
        return self.categoria_sanitaria == 'Vacuna'
    
    def es_desparasitante(self) -> bool:
        """
        Verifica si el item es un desparasitante.
        
        Returns:
            bool: True si es desparasitante
        """
        return self.categoria_sanitaria == 'Desparasitante'
    
    def calcular_fecha_refuerzo(self, fecha_aplicacion: date) -> Optional[date]:
        """
        Calcula la fecha del próximo refuerzo basándose en la fecha de aplicación.
        
        Reglas:
        - Si requiere_refuerzo es False: retorna None
        - Si requiere_refuerzo es True: fecha_aplicacion + dias_refuerzo
        
        Args:
            fecha_aplicacion (date): Fecha en que se aplicó la vacuna
        
        Returns:
            Optional[date]: Fecha del refuerzo o None si no requiere
        
        Example:
            >>> item = Item(1, 'Vacuna X', 'medicamento', 100, requiere_refuerzo=True, dias_refuerzo=21)
            >>> item.calcular_fecha_refuerzo(date(2024, 1, 1))
            date(2024, 1, 22)
        """
        if not self.requiere_refuerzo or self.dias_refuerzo is None:
            return None
        
        return fecha_aplicacion + timedelta(days=self.dias_refuerzo)
    
    def es_vacuna_cria(self) -> bool:
        """
        Identifica si es una vacuna para cría basándose en el nombre.
        
        Busca palabras clave: 'Primera Dosis', 'Cría', 'Becerro'
        
        Returns:
            bool: True si es vacuna de cría
        """
        if not self.es_vacuna():
            return False
        
        nombre_lower = self.nombre.lower()
        palabras_clave = ['primera dosis', 'cría', 'becerro', 'becerra', 'calf']
        
        return any(palabra in nombre_lower for palabra in palabras_clave)
    
    def es_vacuna_brucelosis(self) -> bool:
        """
        Identifica si es la vacuna de Brucelosis.
        
        Returns:
            bool: True si es Brucelosis
        """
        return self.es_vacuna() and 'brucelosis' in self.nombre.lower()
    
    def es_vacuna_rabia(self) -> bool:
        """
        Identifica si es la vacuna de Rabia.
        
        Returns:
            bool: True si es Rabia
        """
        return self.es_vacuna() and 'rabia' in self.nombre.lower()
    
    def es_vacuna_clostridiales(self) -> bool:
        """
        Identifica si es una vacuna de Clostridiales.
        
        Returns:
            bool: True si es Clostridiales
        """
        return self.es_vacuna() and 'clostridial' in self.nombre.lower()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Item a un diccionario.
        
        Returns:
            Dict: Representación en diccionario
        """
        return {
            'id_item': self.id_item,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'costo': float(self.costo),
            'cantidad': float(self.cantidad),
            'dias_retiro_carne': self.dias_retiro_carne,
            'dias_retiro_leche': self.dias_retiro_leche,
            'ingrediente_activo': self.ingrediente_activo,
            'categoria_sanitaria': self.categoria_sanitaria,
            'unidad_medida': self.unidad_medida,
            'requiere_refuerzo': self.requiere_refuerzo,
            'dias_refuerzo': self.dias_refuerzo,
            'es_vacuna': self.es_vacuna()
        }
    
    @staticmethod
    def from_db_row(row: Dict[str, Any]) -> 'Item':
        """
        Crea una instancia de Item desde un registro de base de datos.
        
        Args:
            row (Dict): Diccionario con los datos del item desde la BD
        
        Returns:
            Item: Instancia del item
        """
        return Item(
            id_item=row['id_item'],
            nombre=row['nombre'],
            tipo=row['tipo'],
            costo=row['costo'],
            cantidad=row.get('cantidad', 0.0),
            dias_retiro_carne=row.get('dias_retiro_carne', 0),
            dias_retiro_leche=row.get('dias_retiro_leche', 0),
            ingrediente_activo=row.get('ingrediente_activo'),
            categoria_sanitaria=row.get('categoria_sanitaria', 'NA'),
            unidad_medida=row.get('unidad_medida', 'unidad'),
            requiere_refuerzo=bool(row.get('requiere_refuerzo', False)),
            dias_refuerzo=row.get('dias_refuerzo')
        )
    
    def __repr__(self) -> str:
        """Representación en string del item."""
        return f"Item(nombre='{self.nombre}', tipo='{self.tipo}', categoria='{self.categoria_sanitaria}')"
