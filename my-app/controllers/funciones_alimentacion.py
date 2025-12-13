import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conexion.conexionBD import connectionBD

# --- FÓRMULAS ---

def sql_obtener_formulas():
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM formula ORDER BY nombre ASC"
                cursor.execute(sql)
                formulas = cursor.fetchall()
                
                # Obtener ingredientes para cada fórmula
                for formula in formulas:
                    sql_ing = """
                        SELECT i.nombre, dform.porcentaje 
                        FROM detalle_formula dform
                        JOIN item i ON dform.id_item = i.id_item
                        WHERE dform.id_formula = %s
                    """
                    cursor.execute(sql_ing, (formula['id_formula'],))
                    formula['ingredientes'] = cursor.fetchall()
                    
                return formulas
    except Exception as e:
        print(f"Error en sql_obtener_formulas: {e}")
        return []

def sql_crear_formula(nombre, descripcion, costo, ingredientes):
    """
    ingredientes: lista de dicts [{'id_item': 1, 'porcentaje': 20}, ...]
    """
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Insertar fórmula
                sql = "INSERT INTO formula (nombre, descripcion, costo_estimado) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nombre, descripcion, costo))
                id_formula = cursor.lastrowid
                
                # Insertar ingredientes
                if ingredientes:
                    sql_ing = "INSERT INTO detalle_formula (id_formula, id_item, porcentaje) VALUES (%s, %s, %s)"
                    valores = [(id_formula, ing['id_item'], ing['porcentaje']) for ing in ingredientes]
                    cursor.executemany(sql_ing, valores)
                
                conexion.commit()
                return True
    except Exception as e:
        print(f"Error en sql_crear_formula: {e}")
        return False

def sql_obtener_formula_por_id(id_formula):
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM formula WHERE id_formula = %s"
                cursor.execute(sql, (id_formula,))
                formula = cursor.fetchone()
                
                if formula:
                    sql_ing = """
                        SELECT dform.*, i.nombre 
                        FROM detalle_formula dform
                        JOIN item i ON dform.id_item = i.id_item
                        WHERE dform.id_formula = %s
                    """
                    cursor.execute(sql_ing, (id_formula,))
                    formula['ingredientes'] = cursor.fetchall()
                
                return formula
    except Exception as e:
        print(f"Error en sql_obtener_formula_por_id: {e}")
        return None

def sql_editar_formula(id_formula, nombre, descripcion, costo, ingredientes):
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Actualizar fórmula
                sql = "UPDATE formula SET nombre=%s, descripcion=%s, costo_estimado=%s WHERE id_formula=%s"
                cursor.execute(sql, (nombre, descripcion, costo, id_formula))
                
                # Eliminar ingredientes anteriores
                cursor.execute("DELETE FROM detalle_formula WHERE id_formula = %s", (id_formula,))
                
                # Insertar nuevos ingredientes
                if ingredientes:
                    sql_ing = "INSERT INTO detalle_formula (id_formula, id_item, porcentaje) VALUES (%s, %s, %s)"
                    valores = [(id_formula, ing['id_item'], ing['porcentaje']) for ing in ingredientes]
                    cursor.executemany(sql_ing, valores)
                
                conexion.commit()
                return True
    except Exception as e:
        print(f"Error en sql_editar_formula: {e}")
        return False

# --- REGISTRO DIARIO ---

def sql_registrar_alimentacion_diaria(fecha, id_lote, id_formula, registros):
    """
    registros: lista de dicts [{'id_animal': 1, 'racion_asignada': 5.0, 'racion_consumida': 4.5, 'comentarios': '...'}]
    """
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO registro_alimento 
                    (fecha, id_animal, id_formula_alimento, racion_asignada, racion_consumida, comentarios) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = []
                for reg in registros:
                    valores.append((
                        fecha, 
                        reg['id_animal'], 
                        id_formula, 
                        reg['racion_asignada'], 
                        reg['racion_consumida'], 
                        reg['comentarios']
                    ))
                
                cursor.executemany(sql, valores)
                conexion.commit()
                return True
    except Exception as e:
        print(f"Error en sql_registrar_alimentacion_diaria: {e}")
        return False

def sql_obtener_animales_por_lote(id_lote):
    # Helper para obtener animales de un lote para el formulario
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                # Asumiendo tabla 'animal' con 'id_lote'
                sql = "SELECT id_animal, nombre_numero as nombre FROM animal WHERE id_lote = %s ORDER BY nombre_numero"
                cursor.execute(sql, (id_lote,))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en sql_obtener_animales_por_lote: {e}")
        return []

def sql_obtener_lotes():
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM lote ORDER BY nombre"
                cursor.execute(sql)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en sql_obtener_lotes: {e}")
        return []
