"""
Modelo RegistroSanitario para eventos sanitarios (vacunación, tratamientos, etc).
Incluye cálculo automático de periodos de retiro para seguridad alimentaria.
"""

from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any
from conexion.conexionBD import connectionBD


class RegistroSanitario:
    """
    Representa un registro sanitario (vacunación, desparasitación, tratamiento).
    
    IMPORTANTE: Calcula automáticamente las fechas de liberación para consumo
    basándose en los días de retiro del medicamento aplicado.
    
    Attributes:
        id_registro (int): Identificador único
        fecha (datetime): Fecha y hora del evento
        tipo_evento (str): 'Vacunación', 'Desparasitación', 'Tratamiento', etc.
        responsable (str): Nombre del responsable
        dosis (float): Dosis aplicada
        id_item (int): ID del medicamento/vacuna usado
        id_animal (int): ID del animal tratado
        fecha_proximo_refuerzo (date): Fecha calculada para el refuerzo
        sugerencia_proximo_evento (str): Descripción del próximo evento
        costo_aplicacion (float): Costo de la aplicación
        fecha_liberacion_carne (date): Fecha segura para venta/sacrificio
        fecha_liberacion_leche (date): Fecha segura para consumo de leche
    """
    
    def __init__(
        self,
        id_animal: int,
        id_item: int,
        tipo_evento: str,
        responsable: str,
        dosis: float,
        fecha: Optional[datetime] = None,
        fecha_proximo_refuerzo: Optional[date] = None,
        sugerencia_proximo_evento: Optional[str] = None,
        costo_aplicacion: Optional[float] = None,
        fecha_liberacion_carne: Optional[date] = None,
        fecha_liberacion_leche: Optional[date] = None,
        id_registro: Optional[int] = None
    ):
        self.id_registro = id_registro
        self.fecha = fecha or datetime.now()
        self.tipo_evento = tipo_evento
        self.responsable = responsable
        self.dosis = dosis
        self.id_item = id_item
        self.id_animal = id_animal
        self.fecha_proximo_refuerzo = fecha_proximo_refuerzo
        self.sugerencia_proximo_evento = sugerencia_proximo_evento
        self.costo_aplicacion = costo_aplicacion
        self.fecha_liberacion_carne = fecha_liberacion_carne
        self.fecha_liberacion_leche = fecha_liberacion_leche
    
    def calcular_fechas_liberacion(self, item_data: Dict[str, Any]) -> None:
        """
        Calcula automáticamente las fechas de liberación basándose en el medicamento.
        
        CRÍTICO PARA SEGURIDAD ALIMENTARIA:
        - fecha_liberacion_carne: Fecha segura para venta/sacrificio
        - fecha_liberacion_leche: Fecha segura para consumo de leche
        
        Args:
            item_data (Dict): Diccionario con datos del item/medicamento
                Debe contener: dias_retiro_carne, dias_retiro_leche
        
        Example:
            >>> registro.calcular_fechas_liberacion({
            ...     'dias_retiro_carne': 28,
            ...     'dias_retiro_leche': 7
            ... })
            >>> print(registro.fecha_liberacion_carne)  # fecha + 28 días
        """
        fecha_aplicacion = self.fecha.date() if isinstance(self.fecha, datetime) else self.fecha
        
        # Calcular fecha de liberación para carne
        dias_retiro_carne = item_data.get('dias_retiro_carne', 0)
        if dias_retiro_carne and dias_retiro_carne > 0:
            self.fecha_liberacion_carne = fecha_aplicacion + timedelta(days=dias_retiro_carne)
        else:
            self.fecha_liberacion_carne = None
        
        # Calcular fecha de liberación para leche
        dias_retiro_leche = item_data.get('dias_retiro_leche', 0)
        if dias_retiro_leche and dias_retiro_leche > 0:
            self.fecha_liberacion_leche = fecha_aplicacion + timedelta(days=dias_retiro_leche)
        else:
            self.fecha_liberacion_leche = None
    
    def guardar(self, auto_calcular_retiro: bool = True) -> bool:
        """
        Guarda el registro sanitario en la base de datos.
        
        Si auto_calcular_retiro es True, obtiene los datos del item y calcula
        automáticamente las fechas de liberación antes de guardar.
        
        Args:
            auto_calcular_retiro (bool): Si debe calcular fechas de retiro automáticamente
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        
        Example:
            >>> registro = RegistroSanitario(
            ...     id_animal=1,
            ...     id_item=10,
            ...     tipo_evento='Desparasitación',
            ...     responsable='MVZ. Juan',
            ...     dosis=5.0
            ... )
            >>> registro.guardar()  # Calcula retiros automáticamente
            True
        """
        try:
            # Si se solicita cálculo automático, obtener datos del item
            if auto_calcular_retiro and not self.fecha_liberacion_carne and not self.fecha_liberacion_leche:
                item_data = self._obtener_datos_item()
                if item_data:
                    self.calcular_fechas_liberacion(item_data)
            
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        INSERT INTO registro_sanitario 
                        (fecha, tipo_evento, responsable, dosis, id_item, id_animal, 
                         fecha_proximo_refuerzo, sugerencia_proximo_evento, costo_aplicacion,
                         fecha_liberacion_carne, fecha_liberacion_leche)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    valores = (
                        self.fecha,
                        self.tipo_evento,
                        self.responsable,
                        self.dosis,
                        self.id_item,
                        self.id_animal,
                        self.fecha_proximo_refuerzo,
                        self.sugerencia_proximo_evento,
                        self.costo_aplicacion,
                        self.fecha_liberacion_carne,
                        self.fecha_liberacion_leche
                    )
                    
                    cursor.execute(sql, valores)
                    conexion.commit()
                    
                    # Obtener el ID del registro insertado
                    self.id_registro = cursor.lastrowid
                    
                    return cursor.rowcount > 0
                    
        except Exception as e:
            print(f"Error al guardar registro sanitario: {e}")
            return False
    
    def _obtener_datos_item(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del item desde la base de datos."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = "SELECT dias_retiro_carne, dias_retiro_leche FROM item WHERE id_item = %s"
                    cursor.execute(sql, (self.id_item,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener datos del item: {e}")
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a un diccionario.
        
        Returns:
            Dict: Representación en diccionario
        """
        return {
            'id_registro': self.id_registro,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'tipo_evento': self.tipo_evento,
            'responsable': self.responsable,
            'dosis': float(self.dosis),
            'id_item': self.id_item,
            'id_animal': self.id_animal,
            'fecha_proximo_refuerzo': self.fecha_proximo_refuerzo.isoformat() if self.fecha_proximo_refuerzo else None,
            'sugerencia_proximo_evento': self.sugerencia_proximo_evento,
            'costo_aplicacion': float(self.costo_aplicacion) if self.costo_aplicacion else None,
            'fecha_liberacion_carne': self.fecha_liberacion_carne.isoformat() if self.fecha_liberacion_carne else None,
            'fecha_liberacion_leche': self.fecha_liberacion_leche.isoformat() if self.fecha_liberacion_leche else None
        }
    
    @staticmethod
    def from_db_row(row: Dict[str, Any]) -> 'RegistroSanitario':
        """
        Crea una instancia desde un registro de base de datos.
        
        Args:
            row (Dict): Diccionario con los datos desde la BD
        
        Returns:
            RegistroSanitario: Instancia del registro
        """
        # Convertir fechas si vienen como string
        fecha = row.get('fecha')
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        
        fecha_refuerzo = row.get('fecha_proximo_refuerzo')
        if isinstance(fecha_refuerzo, str):
            fecha_refuerzo = datetime.strptime(fecha_refuerzo, '%Y-%m-%d').date()
        
        fecha_lib_carne = row.get('fecha_liberacion_carne')
        if isinstance(fecha_lib_carne, str):
            fecha_lib_carne = datetime.strptime(fecha_lib_carne, '%Y-%m-%d').date()
        
        fecha_lib_leche = row.get('fecha_liberacion_leche')
        if isinstance(fecha_lib_leche, str):
            fecha_lib_leche = datetime.strptime(fecha_lib_leche, '%Y-%m-%d').date()
        
        return RegistroSanitario(
            id_registro=row.get('id_registro'),
            fecha=fecha,
            tipo_evento=row['tipo_evento'],
            responsable=row['responsable'],
            dosis=row['dosis'],
            id_item=row['id_item'],
            id_animal=row['id_animal'],
            fecha_proximo_refuerzo=fecha_refuerzo,
            sugerencia_proximo_evento=row.get('sugerencia_proximo_evento'),
            costo_aplicacion=row.get('costo_aplicacion'),
            fecha_liberacion_carne=fecha_lib_carne,
            fecha_liberacion_leche=fecha_lib_leche
        )
    
    def __repr__(self) -> str:
        """Representación en string del registro."""
        return f"RegistroSanitario(animal={self.id_animal}, tipo='{self.tipo_evento}', fecha={self.fecha})"
