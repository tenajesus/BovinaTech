# ================================================================
# FUNCIONES PARA GESTIÓN DE INVENTARIO (ELEMENTOS)
# ================================================================

from conexion.conexionBD import connectionBD

# Obtener todos los elementos o filtrados por tipo
def sql_lista_items(tipo_filtro=None):
    """
    Obtiene la lista de items del inventario.
    
    Args:
        tipo_filtro (str, optional): Filtrar por tipo ('medicamento', 'alimento', 'herramienta', 'alimento_preparado')
    
    Returns:
        List[Dict]: Lista de items con todos sus campos
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if tipo_filtro:
                    querySQL = """
                        SELECT 
                            id_item,
                            nombre,
                            tipo,
                            costo,
                            cantidad,
                            minimo,
                            unidad_medida,
                            ingrediente_activo,
                            categoria_sanitaria,
                            dias_retiro_carne,
                            dias_retiro_leche,
                            requiere_refuerzo,
                            dias_refuerzo,
                            CASE
                                WHEN cantidad <= minimo THEN 'bajo'
                                WHEN cantidad <= (minimo * 3) THEN 'medio'
                                ELSE 'alto'
                            END AS nivel_stock
                        FROM item
                        WHERE tipo = %s
                        ORDER BY nombre
                    """
                    cursor.execute(querySQL, (tipo_filtro,))
                else:
                    querySQL = """
                        SELECT 
                            id_item,
                            nombre,
                            tipo,
                            costo,
                            cantidad,
                            minimo,
                            unidad_medida,
                            ingrediente_activo,
                            categoria_sanitaria,
                            dias_retiro_carne,
                            dias_retiro_leche,
                            requiere_refuerzo,
                            dias_refuerzo,
                            CASE
                                WHEN cantidad <= minimo THEN 'bajo'
                                WHEN cantidad <= (minimo * 3) THEN 'medio'
                                ELSE 'alto'
                            END AS nivel_stock
                        FROM item
                        ORDER BY tipo, nombre
                    """
                    cursor.execute(querySQL)
                
                items = cursor.fetchall()
        return items
    except Exception as e:
        print(f"Error en sql_lista_items: {e}")
        return []


# Obtener un item por ID
def sql_obtener_item_por_id(id_item):
    """
    Obtiene un item específico por su ID.
    
    Args:
        id_item (int): ID del item
    
    Returns:
        Dict: Datos del item o None si no existe
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM item WHERE id_item = %s"
                cursor.execute(querySQL, (id_item,))
                item = cursor.fetchone()
        return item
    except Exception as e:
        print(f"Error en sql_obtener_item_por_id: {e}")
        return None


# Registrar nuevo item
def sql_registrar_item(dataForm):
    """
    Registra un nuevo item en el inventario.
    
    Args:
        dataForm: Datos del formulario
    
    Returns:
        bool: True si se registró exitosamente
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Helper para conversión segura
                def safe_float(val, default=0.0):
                    try:
                        return float(val) if val else default
                    except (ValueError, TypeError):
                        return default

                def safe_int(val, default=0):
                    try:
                        return int(val) if val else default
                    except (ValueError, TypeError):
                        return default

                # Campos básicos (siempre presentes)
                nombre = dataForm.get('nombre')
                tipo = dataForm.get('tipo')
                costo = safe_float(dataForm.get('costo'), 0.0)
                cantidad = safe_float(dataForm.get('cantidad'), 0.0)
                minimo = safe_int(dataForm.get('minimo'), 10)
                unidad_medida = dataForm.get('unidad_medida', 'unidad')
                
                # Campos específicos de medicamentos (pueden ser NULL)
                ingrediente_activo = dataForm.get('ingrediente_activo') if dataForm.get('ingrediente_activo') else None
                categoria_sanitaria = dataForm.get('categoria_sanitaria') if dataForm.get('categoria_sanitaria') else None
                dias_retiro_carne = safe_int(dataForm.get('dias_retiro_carne'), 0)
                dias_retiro_leche = safe_int(dataForm.get('dias_retiro_leche'), 0)
                requiere_refuerzo = 1 if dataForm.get('requiere_refuerzo') == 'on' else 0
                dias_refuerzo = safe_int(dataForm.get('dias_refuerzo')) if dataForm.get('dias_refuerzo') else None
                
                sql = """
                    INSERT INTO item 
                    (nombre, tipo, costo, cantidad, minimo, unidad_medida, ingrediente_activo, 
                     categoria_sanitaria, dias_retiro_carne, dias_retiro_leche, 
                     requiere_refuerzo, dias_refuerzo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    nombre, tipo, costo, cantidad, minimo, unidad_medida,
                    ingrediente_activo, categoria_sanitaria,
                    dias_retiro_carne, dias_retiro_leche,
                    requiere_refuerzo, dias_refuerzo
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                
                return cursor.rowcount > 0
                
    except Exception as e:
        print(f"Error en sql_registrar_item: {e}")
        return False


# Actualizar item existente
def sql_actualizar_item(id_item, dataForm):
    """
    Actualiza un item existente.
    
    Args:
        id_item (int): ID del item a actualizar
        dataForm: Datos del formulario
    
    Returns:
        bool: True si se actualizó exitosamente
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Helper para conversión segura
                def safe_float(val, default=0.0):
                    try:
                        return float(val) if val else default
                    except (ValueError, TypeError):
                        return default

                def safe_int(val, default=0):
                    try:
                        return int(val) if val else default
                    except (ValueError, TypeError):
                        return default

                # Campos básicos
                nombre = dataForm.get('nombre')
                tipo = dataForm.get('tipo')
                costo = safe_float(dataForm.get('costo'), 0.0)
                cantidad = safe_float(dataForm.get('cantidad'), 0.0)
                minimo = safe_int(dataForm.get('minimo'), 10)
                unidad_medida = dataForm.get('unidad_medida', 'unidad')
                
                # Campos específicos de medicamentos
                ingrediente_activo = dataForm.get('ingrediente_activo') if dataForm.get('ingrediente_activo') else None
                categoria_sanitaria = dataForm.get('categoria_sanitaria') if dataForm.get('categoria_sanitaria') else None
                dias_retiro_carne = safe_int(dataForm.get('dias_retiro_carne'), 0)
                dias_retiro_leche = safe_int(dataForm.get('dias_retiro_leche'), 0)
                requiere_refuerzo = 1 if dataForm.get('requiere_refuerzo') == 'on' else 0
                dias_refuerzo = safe_int(dataForm.get('dias_refuerzo')) if dataForm.get('dias_refuerzo') else None
                
                sql = """
                    UPDATE item SET
                        nombre = %s,
                        tipo = %s,
                        costo = %s,
                        cantidad = %s,
                        minimo = %s,
                        unidad_medida = %s,
                        ingrediente_activo = %s,
                        categoria_sanitaria = %s,
                        dias_retiro_carne = %s,
                        dias_retiro_leche = %s,
                        requiere_refuerzo = %s,
                        dias_refuerzo = %s
                    WHERE id_item = %s
                """
                
                valores = (
                    nombre, tipo, costo, cantidad, minimo, unidad_medida,
                    ingrediente_activo, categoria_sanitaria,
                    dias_retiro_carne, dias_retiro_leche,
                    requiere_refuerzo, dias_refuerzo,
                    id_item
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                
                return cursor.rowcount > 0
                
    except Exception as e:
        print(f"Error en sql_actualizar_item: {e}")
        return False


# Eliminar item
def sql_eliminar_item(id_item):
    """
    Elimina un item del inventario.
    
    Args:
        id_item (int): ID del item a eliminar
    
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "DELETE FROM item WHERE id_item = %s"
                cursor.execute(sql, (id_item,))
                conexion_MySQLdb.commit()
                
                return cursor.rowcount > 0
                
    except Exception as e:
        print(f"Error en sql_eliminar_item: {e}")
        return False


# Obtener estadísticas de inventario
def sql_estadisticas_inventario():
    """
    Obtiene estadísticas generales del inventario.
    
    Returns:
        Dict: Estadísticas del inventario
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        COUNT(*) as total_items,
                        SUM(CASE WHEN tipo = 'medicamento' THEN 1 ELSE 0 END) as total_medicamentos,
                        SUM(CASE WHEN tipo = 'alimento' THEN 1 ELSE 0 END) as total_alimentos,
                        SUM(CASE WHEN tipo = 'herramienta' THEN 1 ELSE 0 END) as total_herramientas,
                        SUM(CASE WHEN cantidad < 10 THEN 1 ELSE 0 END) as items_stock_bajo,
                        SUM(costo * cantidad) as valor_total_inventario
                    FROM item
                """
                cursor.execute(querySQL)
                stats = cursor.fetchone()
        return stats
    except Exception as e:
        print(f"Error en sql_estadisticas_inventario: {e}")
        return {
            'total_items': 0,
            'total_medicamentos': 0,
            'total_alimentos': 0,
            'total_herramientas': 0,
            'items_stock_bajo': 0,
            'valor_total_inventario': 0
        }
