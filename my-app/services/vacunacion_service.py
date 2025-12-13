"""
Servicio de Vacunación con lógica de negocio veterinaria.

Este módulo implementa las reglas de negocio para el cálculo automático
de esquemas de vacunación basados en la edad del animal y su historial.

Reglas Veterinarias Implementadas:
1. Becerros 2-3 meses (60-90 días): Primera Dosis + Refuerzo a 21 días
2. Hembras 4-6 meses (120-180 días): Brucelosis obligatoria
3. Destete 6-8 meses (180-240 días): Refuerzo general
4. Adultos: Rabia/Clostridiales con refuerzo anual (365 días)
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
from conexion.conexionBD import connectionBD
from models.animal import Animal
from models.item import Item
from models.registro_sanitario import RegistroSanitario


class VacunacionService:
    """
    Servicio centralizado para la gestión de vacunación automática.
    
    Implementa la lógica de negocio veterinaria para calcular alertas
    y registrar vacunaciones con cálculo automático de refuerzos.
    """
    
    @staticmethod
    def calcular_proximo_evento_sanitario(animal_id: int) -> List[Dict[str, Any]]:
        """
        Calcula los próximos eventos sanitarios sugeridos para un animal.
        
        Analiza la edad del animal y su historial de vacunación para
        determinar qué vacunas debe recibir según las reglas veterinarias.
        
        Args:
            animal_id (int): ID del animal a analizar
        
        Returns:
            List[Dict]: Lista de eventos sugeridos con estructura:
                {
                    'titulo': str,           # Nombre de la vacuna/evento
                    'urgencia': str,         # 'Alta', 'Media', 'Baja'
                    'fecha_sugerida': date,  # Fecha sugerida de aplicación
                    'descripcion': str,      # Descripción detallada
                    'dias_edad': int         # Edad del animal en días
                }
        
        Example:
            >>> alertas = VacunacionService.calcular_proximo_evento_sanitario(1)
            >>> print(alertas[0]['titulo'])
            'Primera Dosis: Clostridiales + Viral Respiratoria'
        """
        alertas = []
        
        try:
            # Obtener datos del animal
            animal = VacunacionService._obtener_animal(animal_id)
            if not animal:
                return alertas
            
            # Obtener historial sanitario del animal
            historial = VacunacionService._obtener_historial_sanitario(animal_id)
            
            # Calcular edad en días
            edad_dias = animal.edad_en_dias()
            fecha_actual = date.today()
            
            # ============================================================
            # REGLA 1: Becerros 2-3 meses (60-90 días)
            # Primera Dosis: Clostridiales + Viral Respiratoria
            # ============================================================
            if 60 <= edad_dias <= 90:
                # Verificar si ya tiene la primera dosis
                tiene_primera_dosis = VacunacionService._tiene_vacuna_tipo(
                    historial, 'primera dosis'
                )
                
                if not tiene_primera_dosis:
                    alertas.append({
                        'titulo': 'Primera Dosis: Clostridiales + Viral Respiratoria',
                        'urgencia': 'Alta',
                        'fecha_sugerida': fecha_actual,
                        'descripcion': 'Vacunación inicial para becerros de 2-3 meses. Requiere refuerzo a los 21 días.',
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'vacuna_cria'
                    })
                
                # Verificar si necesita desparasitación
                tiene_desparasitacion_reciente = VacunacionService._tiene_evento_reciente(
                    historial, 'Desparasitación', dias=60
                )
                
                if not tiene_desparasitacion_reciente:
                    alertas.append({
                        'titulo': 'Desparasitación',
                        'urgencia': 'Media',
                        'fecha_sugerida': fecha_actual,
                        'descripcion': 'Desparasitación recomendada para becerros en crecimiento.',
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'desparasitacion'
                    })
            
            # ============================================================
            # REGLA 2: Hembras 4-6 meses (120-180 días)
            # Brucelosis obligatoria
            # ============================================================
            if 120 <= edad_dias <= 180 and animal.es_hembra():
                tiene_brucelosis = VacunacionService._tiene_vacuna_tipo(
                    historial, 'brucelosis'
                )
                
                if not tiene_brucelosis:
                    alertas.append({
                        'titulo': 'Obligatoria: Brucelosis RB51',
                        'urgencia': 'Alta',
                        'fecha_sugerida': fecha_actual,
                        'descripcion': 'Vacuna obligatoria para hembras de 4-6 meses según normativa oficial (NOM-041-ZOO-1995).',
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'brucelosis'
                    })
            
            # ============================================================
            # REGLA 3: Destete 6-8 meses (180-240 días)
            # Refuerzo general al destete
            # ============================================================
            if 180 <= edad_dias <= 240:
                tiene_refuerzo_destete = VacunacionService._tiene_vacuna_tipo(
                    historial, 'refuerzo'
                ) or VacunacionService._tiene_vacuna_tipo(
                    historial, 'destete'
                )
                
                if not tiene_refuerzo_destete:
                    alertas.append({
                        'titulo': 'Refuerzo General al Destete',
                        'urgencia': 'Media',
                        'fecha_sugerida': fecha_actual,
                        'descripcion': 'Refuerzo de vacunas al momento del destete (6-8 meses).',
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'refuerzo_destete'
                    })
                
                # Desparasitación al destete
                tiene_desparasitacion_destete = VacunacionService._tiene_evento_reciente(
                    historial, 'Desparasitación', dias=30
                )
                
                if not tiene_desparasitacion_destete:
                    alertas.append({
                        'titulo': 'Desparasitación al Destete',
                        'urgencia': 'Media',
                        'fecha_sugerida': fecha_actual,
                        'descripcion': 'Desparasitación recomendada al momento del destete.',
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'desparasitacion'
                    })
            
            # ============================================================
            # REGLA 4: Adultos (>540 días / >18 meses)
            # Verificar refuerzos anuales pendientes
            # ============================================================
            if edad_dias > 540:
                # Verificar refuerzos pendientes
                refuerzos_pendientes = VacunacionService._obtener_refuerzos_pendientes(
                    historial, fecha_actual
                )
                
                for refuerzo in refuerzos_pendientes:
                    dias_vencido = (fecha_actual - refuerzo['fecha_refuerzo']).days
                    
                    if dias_vencido > 0:
                        urgencia = 'Alta' if dias_vencido > 30 else 'Media'
                    else:
                        urgencia = 'Baja'
                    
                    alertas.append({
                        'titulo': f"Refuerzo: {refuerzo['vacuna']}",
                        'urgencia': urgencia,
                        'fecha_sugerida': refuerzo['fecha_refuerzo'],
                        'descripcion': f"Refuerzo programado para {refuerzo['vacuna']}.",
                        'dias_edad': edad_dias,
                        'tipo_alerta': 'refuerzo_adulto',
                        'dias_vencido': dias_vencido if dias_vencido > 0 else 0
                    })
            
            return alertas
            
        except Exception as e:
            print(f"Error al calcular eventos sanitarios para animal {animal_id}: {e}")
            return []
    
    @staticmethod
    def registrar_vacunacion(
        id_animal: int,
        id_item: int,
        dosis: float,
        responsable: str,
        fecha_aplicacion: Optional[date] = None,
        tipo_evento: str = 'Vacunación'
    ) -> bool:
        """
        Registra una vacunación y calcula automáticamente el refuerzo.
        
        Esta función:
        1. Obtiene información de la vacuna (Item)
        2. Calcula la fecha del próximo refuerzo si aplica
        3. Guarda el registro en la base de datos
        
        Args:
            id_animal (int): ID del animal
            id_item (int): ID de la vacuna/medicamento
            dosis (float): Dosis aplicada
            responsable (str): Nombre del responsable
            fecha_aplicacion (date, optional): Fecha de aplicación. Default: hoy
            tipo_evento (str): Tipo de evento. Default: 'Vacunación'
        
        Returns:
            bool: True si se registró exitosamente
        
        Example:
            >>> VacunacionService.registrar_vacunacion(
            ...     id_animal=1,
            ...     id_item=10,
            ...     dosis=5.0,
            ...     responsable='MVZ. Juan'
            ... )
            True
        """
        try:
            # Obtener información del item (vacuna)
            item = VacunacionService._obtener_item(id_item)
            if not item:
                print(f"Item {id_item} no encontrado")
                return False
            
            # Fecha de aplicación
            if fecha_aplicacion is None:
                fecha_aplicacion = date.today()
            
            # Convertir fecha a datetime para el registro
            fecha_datetime = datetime.combine(fecha_aplicacion, datetime.now().time())
            
            # Calcular fecha de refuerzo si la vacuna lo requiere
            fecha_refuerzo = None
            sugerencia = None
            
            if item.requiere_refuerzo and item.dias_refuerzo:
                fecha_refuerzo = item.calcular_fecha_refuerzo(fecha_aplicacion)
                sugerencia = f"Refuerzo programado para {fecha_refuerzo.strftime('%d/%m/%Y')}"
            
            # Crear registro sanitario
            registro = RegistroSanitario(
                id_animal=id_animal,
                id_item=id_item,
                tipo_evento=tipo_evento,
                responsable=responsable,
                dosis=dosis,
                fecha=fecha_datetime,
                fecha_proximo_refuerzo=fecha_refuerzo,
                sugerencia_proximo_evento=sugerencia,
                costo_aplicacion=item.costo if item else None
            )
            
            # Guardar en base de datos
            resultado = registro.guardar()
            
            if resultado:
                print(f"✓ Vacunación registrada exitosamente para animal {id_animal}")
                if fecha_refuerzo:
                    print(f"  → Refuerzo programado para: {fecha_refuerzo.strftime('%d/%m/%Y')}")
            
            return resultado
            
        except Exception as e:
            print(f"Error al registrar vacunación: {e}")
            return False
    
    @staticmethod
    def obtener_alertas_dashboard() -> Dict[str, Any]:
        """
        Obtiene un resumen de alertas sanitarias para el dashboard.
        
        Calcula alertas para todos los animales y las agrupa por urgencia.
        
        Returns:
            Dict: Resumen de alertas con estructura:
                {
                    'total_alertas': int,
                    'alta_urgencia': int,
                    'media_urgencia': int,
                    'baja_urgencia': int,
                    'alertas_por_animal': List[Dict]
                }
        """
        try:
            # Obtener todos los animales
            animales = VacunacionService._obtener_todos_animales()
            
            total_alta = 0
            total_media = 0
            total_baja = 0
            alertas_por_animal = []
            
            for animal_data in animales:
                animal_id = animal_data['id_animal']
                alertas = VacunacionService.calcular_proximo_evento_sanitario(animal_id)
                
                if alertas:
                    # Contar por urgencia
                    alta = sum(1 for a in alertas if a['urgencia'] == 'Alta')
                    media = sum(1 for a in alertas if a['urgencia'] == 'Media')
                    baja = sum(1 for a in alertas if a['urgencia'] == 'Baja')
                    
                    total_alta += alta
                    total_media += media
                    total_baja += baja
                    
                    alertas_por_animal.append({
                        'animal': {
                            'id': animal_id,
                            'arete': animal_data['arete'],
                            'raza': animal_data.get('raza'),
                            'edad_meses': animal_data.get('edad_meses', 0)
                        },
                        'alertas': alertas,
                        'total_alertas': len(alertas),
                        'urgencia_maxima': 'Alta' if alta > 0 else ('Media' if media > 0 else 'Baja')
                    })
            
            return {
                'total_alertas': total_alta + total_media + total_baja,
                'alta_urgencia': total_alta,
                'media_urgencia': total_media,
                'baja_urgencia': total_baja,
                'alertas_por_animal': alertas_por_animal
            }
            
        except Exception as e:
            print(f"Error al obtener alertas del dashboard: {e}")
            return {
                'total_alertas': 0,
                'alta_urgencia': 0,
                'media_urgencia': 0,
                'baja_urgencia': 0,
                'alertas_por_animal': []
            }
    
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
    def _obtener_item(item_id: int) -> Optional[Item]:
        """Obtiene un item de la base de datos."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = "SELECT * FROM item WHERE id_item = %s"
                    cursor.execute(sql, (item_id,))
                    row = cursor.fetchone()
                    
                    if row:
                        return Item.from_db_row(row)
                    return None
        except Exception as e:
            print(f"Error al obtener item {item_id}: {e}")
            return None
    
    @staticmethod
    def _obtener_historial_sanitario(animal_id: int) -> List[Dict[str, Any]]:
        """Obtiene el historial sanitario completo de un animal."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT rs.*, i.nombre as nombre_item, i.categoria_sanitaria
                        FROM registro_sanitario rs
                        INNER JOIN item i ON rs.id_item = i.id_item
                        WHERE rs.id_animal = %s
                        ORDER BY rs.fecha DESC
                    """
                    cursor.execute(sql, (animal_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial sanitario: {e}")
            return []
    
    @staticmethod
    def _obtener_todos_animales() -> List[Dict[str, Any]]:
        """Obtiene todos los animales con información básica."""
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            id_animal, 
                            arete, 
                            raza, 
                            sexo,
                            fecha_nacimiento,
                            TIMESTAMPDIFF(DAY, fecha_nacimiento, CURDATE()) as edad_dias,
                            TIMESTAMPDIFF(MONTH, fecha_nacimiento, CURDATE()) as edad_meses
                        FROM animal
                        WHERE fecha_nacimiento IS NOT NULL
                        ORDER BY arete
                    """
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener animales: {e}")
            return []
    
    @staticmethod
    def _tiene_vacuna_tipo(historial: List[Dict], tipo: str) -> bool:
        """Verifica si el animal tiene una vacuna de cierto tipo en su historial."""
        for registro in historial:
            nombre_item = registro.get('nombre_item', '').lower()
            if tipo.lower() in nombre_item:
                return True
        return False
    
    @staticmethod
    def _tiene_evento_reciente(historial: List[Dict], tipo_evento: str, dias: int) -> bool:
        """Verifica si el animal tiene un evento reciente (últimos X días)."""
        fecha_limite = date.today() - timedelta(days=dias)
        
        for registro in historial:
            if registro.get('tipo_evento') == tipo_evento:
                fecha_registro = registro.get('fecha')
                if isinstance(fecha_registro, str):
                    fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d %H:%M:%S').date()
                elif isinstance(fecha_registro, datetime):
                    fecha_registro = fecha_registro.date()
                
                if fecha_registro and fecha_registro >= fecha_limite:
                    return True
        return False
    
    @staticmethod
    def _obtener_refuerzos_pendientes(historial: List[Dict], fecha_actual: date) -> List[Dict]:
        """Obtiene los refuerzos pendientes o próximos a vencer."""
        refuerzos = []
        
        for registro in historial:
            fecha_refuerzo = registro.get('fecha_proximo_refuerzo')
            
            if fecha_refuerzo:
                if isinstance(fecha_refuerzo, str):
                    fecha_refuerzo = datetime.strptime(fecha_refuerzo, '%Y-%m-%d').date()
                
                # Considerar refuerzos desde 30 días antes hasta vencidos
                fecha_inicio = fecha_actual - timedelta(days=30)
                
                if fecha_refuerzo >= fecha_inicio:
                    refuerzos.append({
                        'vacuna': registro.get('nombre_item', 'Vacuna'),
                        'fecha_refuerzo': fecha_refuerzo,
                        'id_registro': registro.get('id_registro')
                    })
        
        return refuerzos
