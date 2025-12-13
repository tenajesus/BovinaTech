"""
Servicio de Desparasitación y Validación de Periodos de Retiro.

Este módulo implementa la lógica crítica de seguridad alimentaria para:
1. Sugerir desparasitaciones según edad y estacionalidad
2. Validar periodos de retiro antes de ventas/ordeños
3. Prevenir consumo de productos durante periodos inseguros

IMPORTANTE: Este servicio es CRÍTICO para la seguridad alimentaria.
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from conexion.conexionBD import connectionBD
from models.animal import Animal


class DesparasitacionService:
    """
    Servicio para gestión de desparasitaciones y validación de periodos de retiro.
    
    FUNCIONES CRÍTICAS DE SEGURIDAD:
    - validar_apto_consumo(): Previene ventas/ordeños durante retiro
    - sugerir_desparasitacion(): Calendario automático por edad/estación
    """
    
    @staticmethod
    def validar_apto_consumo(
        animal_id: int,
        tipo_producto: str = 'carne'
    ) -> Tuple[bool, Optional[str]]:
        """
        🚨 FUNCIÓN CRÍTICA DE SEGURIDAD ALIMENTARIA 🚨
        
        Valida si un animal está apto para consumo (venta o ordeño).
        Verifica el último tratamiento y sus periodos de retiro.
        
        Args:
            animal_id (int): ID del animal a validar
            tipo_producto (str): 'carne' o 'leche'
        
        Returns:
            Tuple[bool, Optional[str]]: 
                - bool: True si es seguro, False si está en retiro
                - str: Mensaje de alerta si está en retiro, None si es seguro
        
        Example:
            >>> apto, mensaje = DesparasitacionService.validar_apto_consumo(1, 'carne')
            >>> if not apto:
            ...     print(f"BLOQUEADO: {mensaje}")
            BLOQUEADO: PELIGRO: Animal en periodo de retiro por Ivermectina. Faltan 5 días.
        """
        try:
            # Obtener el último tratamiento del animal
            ultimo_tratamiento = DesparasitacionService._obtener_ultimo_tratamiento(animal_id)
            
            if not ultimo_tratamiento:
                # Sin tratamientos previos = seguro
                return True, None
            
            fecha_actual = date.today()
            
            # Determinar qué fecha de liberación verificar
            if tipo_producto.lower() == 'carne':
                fecha_liberacion = ultimo_tratamiento.get('fecha_liberacion_carne')
            elif tipo_producto.lower() == 'leche':
                fecha_liberacion = ultimo_tratamiento.get('fecha_liberacion_leche')
            else:
                return False, f"Tipo de producto inválido: {tipo_producto}"
            
            # Si no hay fecha de liberación = no hay retiro = seguro
            if not fecha_liberacion:
                return True, None
            
            # Convertir a date si viene como string
            if isinstance(fecha_liberacion, str):
                fecha_liberacion = datetime.strptime(fecha_liberacion, '%Y-%m-%d').date()
            
            # Verificar si aún está en periodo de retiro
            if fecha_actual < fecha_liberacion:
                dias_faltantes = (fecha_liberacion - fecha_actual).days
                nombre_medicamento = ultimo_tratamiento.get('nombre_medicamento', 'Medicamento')
                
                mensaje_alerta = (
                    f"🚨 PELIGRO: Animal en periodo de retiro por {nombre_medicamento}. "
                    f"Faltan {dias_faltantes} día{'s' if dias_faltantes != 1 else ''} "
                    f"(Liberación: {fecha_liberacion.strftime('%d/%m/%Y')})"
                )
                
                return False, mensaje_alerta
            
            # Fecha de liberación ya pasó = seguro
            return True, None
            
        except Exception as e:
            print(f"Error al validar apto para consumo: {e}")
            # En caso de error, por seguridad retornar False
            return False, f"Error al validar seguridad del animal: {str(e)}"
    
    @staticmethod
    def sugerir_desparasitacion(animal_id: int) -> List[Dict[str, Any]]:
        """
        Calcula sugerencias de desparasitación basadas en edad y estacionalidad.
        
        Reglas Implementadas:
        1. Por Edad:
           - 60-90 días: Desparasitación Inicial (Interna/Vitaminas)
           - 6-8 meses (Destete): Desparasitación Completa (Ivermectina)
        
        2. Por Estacionalidad:
           - Mayo/Junio (Inicio Lluvias): Baño contra Garrapatas
           - Noviembre/Diciembre (Fin Lluvias): Control Fasciola Hepática
        
        Args:
            animal_id (int): ID del animal
        
        Returns:
            List[Dict]: Lista de sugerencias con estructura:
                {
                    'titulo': str,
                    'tipo': str,  # 'edad' o 'estacional'
                    'urgencia': str,  # 'Alta', 'Media', 'Baja'
                    'descripcion': str,
                    'medicamento_sugerido': str
                }
        """
        sugerencias = []
        
        try:
            # Obtener datos del animal
            animal = DesparasitacionService._obtener_animal(animal_id)
            if not animal:
                return sugerencias
            
            edad_dias = animal.edad_en_dias()
            fecha_actual = date.today()
            mes_actual = fecha_actual.month
            
            # Obtener historial de desparasitaciones
            historial = DesparasitacionService._obtener_historial_desparasitacion(animal_id)
            
            # ============================================================
            # REGLA 1: Becerros 60-90 días - Desparasitación Inicial
            # ============================================================
            if 60 <= edad_dias <= 90:
                tiene_inicial = DesparasitacionService._tiene_desparasitacion_tipo(
                    historial, 'inicial', dias_recientes=30
                )
                
                if not tiene_inicial:
                    sugerencias.append({
                        'titulo': 'Desparasitación Inicial (Interna + Vitaminas)',
                        'tipo': 'edad',
                        'urgencia': 'Alta',
                        'descripcion': 'Desparasitación inicial para becerros de 2-3 meses. Incluye vitaminas para fortalecer sistema inmune.',
                        'medicamento_sugerido': 'Levamisol + Vitaminas',
                        'edad_dias': edad_dias
                    })
            
            # ============================================================
            # REGLA 2: Destete 6-8 meses - Desparasitación Completa
            # ============================================================
            if 180 <= edad_dias <= 240:
                tiene_destete = DesparasitacionService._tiene_desparasitacion_tipo(
                    historial, 'ivermectina', dias_recientes=60
                )
                
                if not tiene_destete:
                    sugerencias.append({
                        'titulo': 'Desparasitación Completa al Destete',
                        'tipo': 'edad',
                        'urgencia': 'Alta',
                        'descripcion': 'Desparasitación completa con Ivermectina al momento del destete (6-8 meses). Controla parásitos internos y externos.',
                        'medicamento_sugerido': 'Ivermectina 1%',
                        'edad_dias': edad_dias
                    })
            
            # ============================================================
            # REGLA 3: Mayo/Junio - Inicio de Lluvias (Garrapatas)
            # ============================================================
            if mes_actual in [5, 6]:  # Mayo, Junio
                tiene_garrapatas = DesparasitacionService._tiene_desparasitacion_tipo(
                    historial, 'garrapata', dias_recientes=90
                )
                
                if not tiene_garrapatas:
                    sugerencias.append({
                        'titulo': 'Baño contra Garrapatas (Externo)',
                        'tipo': 'estacional',
                        'urgencia': 'Media',
                        'descripcion': 'Control de garrapatas al inicio de temporada de lluvias. Previene enfermedades transmitidas por garrapatas.',
                        'medicamento_sugerido': 'Baño Garrapaticida (Amitraz)',
                        'estacion': 'Inicio Lluvias',
                        'edad_dias': edad_dias
                    })
            
            # ============================================================
            # REGLA 4: Noviembre/Diciembre - Fin de Lluvias (Fasciola)
            # ============================================================
            if mes_actual in [11, 12]:  # Noviembre, Diciembre
                tiene_fasciola = DesparasitacionService._tiene_desparasitacion_tipo(
                    historial, 'fasciola', dias_recientes=120
                )
                
                if not tiene_fasciola:
                    sugerencias.append({
                        'titulo': 'Control Fasciola Hepática (Interno)',
                        'tipo': 'estacional',
                        'urgencia': 'Media',
                        'descripcion': 'Control de Fasciola hepática al final de temporada de lluvias. Previene daño hepático.',
                        'medicamento_sugerido': 'Albendazol',
                        'estacion': 'Fin Lluvias',
                        'edad_dias': edad_dias
                    })
            
            # ============================================================
            # REGLA 5: Adultos - Desparasitación Semestral
            # ============================================================
            if edad_dias > 540:  # Más de 18 meses
                ultima_desparasitacion = DesparasitacionService._dias_desde_ultima_desparasitacion(historial)
                
                if ultima_desparasitacion is None or ultima_desparasitacion > 180:
                    sugerencias.append({
                        'titulo': 'Desparasitación Semestral (Adultos)',
                        'tipo': 'edad',
                        'urgencia': 'Baja' if ultima_desparasitacion and ultima_desparasitacion < 210 else 'Media',
                        'descripcion': 'Desparasitación de mantenimiento para adultos. Recomendada cada 6 meses.',
                        'medicamento_sugerido': 'Ivermectina 1%',
                        'edad_dias': edad_dias,
                        'dias_desde_ultima': ultima_desparasitacion
                    })
            
            return sugerencias
            
        except Exception as e:
            print(f"Error al sugerir desparasitación para animal {animal_id}: {e}")
            return []
    
    @staticmethod
    def obtener_animales_en_retiro(tipo_producto: str = 'carne') -> List[Dict[str, Any]]:
        """
        Obtiene lista de animales que actualmente están en periodo de retiro.
        
        Útil para dashboards y reportes de seguridad.
        
        Args:
            tipo_producto (str): 'carne' o 'leche'
        
        Returns:
            List[Dict]: Lista de animales en retiro con información detallada
        """
        animales_en_retiro = []
        
        try:
            # Obtener todos los animales con tratamientos activos
            animales = DesparasitacionService._obtener_animales_con_tratamientos()
            
            for animal_data in animales:
                animal_id = animal_data['id_animal']
                apto, mensaje = DesparasitacionService.validar_apto_consumo(animal_id, tipo_producto)
                
                if not apto:
                    animales_en_retiro.append({
                        'id_animal': animal_id,
                        'arete': animal_data.get('arete'),
                        'raza': animal_data.get('raza'),
                        'mensaje_alerta': mensaje,
                        'tipo_producto': tipo_producto
                    })
            
            return animales_en_retiro
            
        except Exception as e:
            print(f"Error al obtener animales en retiro: {e}")
            return []
    
    # ================================================================
    # MÉTODOS PRIVADOS DE UTILIDAD
    # ================================================================
    
    @staticmethod
    def _obtener_animal(animal_id: int) -> Optional[Animal]:
        """Obtiene un animal de la base de datos."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = "SELECT * FROM animal WHERE id_animal = %s"
                    cursor.execute(sql, (animal_id,))
                    row = cursor.fetchone()
                    
                    if row:
                        return Animal.from_db_row(row)
                    return None
        except Exception as e:
            print(f"Error al obtener animal {animal_id}: {e}")
            return None
    
    @staticmethod
    def _obtener_ultimo_tratamiento(animal_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene el último tratamiento aplicado al animal."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            rs.*,
                            i.nombre as nombre_medicamento,
                            i.dias_retiro_carne,
                            i.dias_retiro_leche
                        FROM registro_sanitario rs
                        INNER JOIN item i ON rs.id_item = i.id_item
                        WHERE rs.id_animal = %s
                        AND (i.dias_retiro_carne > 0 OR i.dias_retiro_leche > 0)
                        ORDER BY rs.fecha DESC
                        LIMIT 1
                    """
                    cursor.execute(sql, (animal_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener último tratamiento: {e}")
            return None
    
    @staticmethod
    def _obtener_historial_desparasitacion(animal_id: int) -> List[Dict[str, Any]]:
        """Obtiene el historial de desparasitaciones del animal."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT rs.*, i.nombre as nombre_medicamento
                        FROM registro_sanitario rs
                        INNER JOIN item i ON rs.id_item = i.id_item
                        WHERE rs.id_animal = %s
                        AND (rs.tipo_evento = 'Desparasitación' OR i.categoria_sanitaria = 'Desparasitante')
                        ORDER BY rs.fecha DESC
                    """
                    cursor.execute(sql, (animal_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial de desparasitación: {e}")
            return []
    
    @staticmethod
    def _obtener_animales_con_tratamientos() -> List[Dict[str, Any]]:
        """Obtiene todos los animales que tienen tratamientos registrados."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT DISTINCT a.id_animal, a.arete, a.raza
                        FROM animal a
                        INNER JOIN registro_sanitario rs ON a.id_animal = rs.id_animal
                        ORDER BY a.arete
                    """
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener animales con tratamientos: {e}")
            return []
    
    @staticmethod
    def _tiene_desparasitacion_tipo(
        historial: List[Dict],
        tipo: str,
        dias_recientes: int = 90
    ) -> bool:
        """Verifica si el animal tiene una desparasitación de cierto tipo reciente."""
        fecha_limite = date.today() - timedelta(days=dias_recientes)
        
        for registro in historial:
            nombre_med = registro.get('nombre_medicamento', '').lower()
            
            # Verificar por tipo
            if tipo.lower() in nombre_med:
                fecha_reg = registro.get('fecha')
                if isinstance(fecha_reg, str):
                    fecha_reg = datetime.strptime(fecha_reg, '%Y-%m-%d %H:%M:%S').date()
                elif isinstance(fecha_reg, datetime):
                    fecha_reg = fecha_reg.date()
                
                if fecha_reg and fecha_reg >= fecha_limite:
                    return True
        
        return False
    
    @staticmethod
    def _dias_desde_ultima_desparasitacion(historial: List[Dict]) -> Optional[int]:
        """Calcula días desde la última desparasitación."""
        if not historial:
            return None
        
        # El historial ya viene ordenado por fecha DESC
        ultimo = historial[0]
        fecha_ultimo = ultimo.get('fecha')
        
        if isinstance(fecha_ultimo, str):
            fecha_ultimo = datetime.strptime(fecha_ultimo, '%Y-%m-%d %H:%M:%S').date()
        elif isinstance(fecha_ultimo, datetime):
            fecha_ultimo = fecha_ultimo.date()
        
        if fecha_ultimo:
            return (date.today() - fecha_ultimo).days
        
        return None
