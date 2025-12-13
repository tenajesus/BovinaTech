from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

# Importar servicios
from services.desparasitacion_service import DesparasitacionService

PATH_URL = "public/empleados"
PATH_URL_2 = "public/particular"
PATH_URL_3 = "public/oficial"

# ============================================================================
# ALL ROUTES BELOW ARE COMMENTED OUT BECAUSE THEY REFERENCE NON-EXISTENT TABLES
# The database 'ganaderia_app' does not have these tables:
# - comisiones_particular
# - comisiones_oficial  
# - tbl_empleados
# ============================================================================

'''
@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')\n        return redirect(url_for('inicio'))

@app.route('/registrar-oficial', methods=['GET'])
def viewFormOficial():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_3}/form_oficial.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/registrar-particular', methods=['GET'])
def viewFormParticular():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_2}/form_particular.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_empleados'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# registro de salida particular

@app.route('/form-registrar-particular', methods=['POST'])
def formParticular():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_particular(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_particular'))
            else:
                flash('La salida no ha sido registrada.', 'error')
                return render_template(f'{PATH_URL_2}/form_particular.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# registro de salida oficial

@app.route('/form-registrar-oficial', methods=['POST'])
def formOficial():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_oficial(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_oficial'))
            else:
                flash('La salida no ha sido registrada.', 'error')
                return render_template(f'{PATH_URL_3}/form_oficial.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/lista-particular', methods=['GET'])
def lista_particular():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_2}/lista_particular.html', particular=sql_lista_particulares())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/lista-oficial', methods=['GET'])
def lista_oficial():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_3}/lista_oficial.html', oficiales=sql_lista_oficiales())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado) or []
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#detalle Oficiales

@app.route("/detalles-oficial/", methods=['GET'])
@app.route("/detalles-oficial/<int:id>", methods=['GET'])
def detalleOficial(id=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if id is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_salidas(id) or []
            return render_template(f'{PATH_URL_3}/detalles_oficial.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
#detalle Particulares

@app.route("/detalles-particular/", methods=['GET'])
@app.route("/detalles-particular/<int:id>", methods=['GET'])
def detalleParticular(id=None):
    if 'conectado' in session:
        # Verificamos si el parámetro id es None o no está presente en la URL
        if id is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_part(id) or []
            return render_template(f'{PATH_URL_2}/detalles_particular.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Buscador de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Buscador oficial
@app.route("/buscando-oficial", methods=['POST'])
def viewBuscarOficial():
    resultadoBusqueda = buscarOficialBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_3}/resultado_busqueda_oficial.html', dataBusquedaof=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Buscador particular
@app.route("/buscando-particular", methods=['POST'])
def viewBuscarParticular():
    resultadoBusqueda = buscarParticular(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_2}/resultado_busqueda_particular.html', dataBusquedapa=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_empleados'))

@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))

@app.route('/borrar-empleado/<string:id_empleado>/<string:foto_empleado>', methods=['GET'])
def borrarEmpleado(id_empleado, foto_empleado):
    resp = eliminarEmpleado(id_empleado, foto_empleado)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
'''


# Ruta para Salud y Tratamientos
@app.route('/salud-tratamientos', methods=['GET'])
def salud_tratamientos():
    if 'conectado' in session:
        registros = sql_lista_registros_sanitarios()
        animales = sql_lista_animales()
        lotes = sql_lista_lotes()
        medicamentos = sql_lista_medicamentos()
        return render_template('salud/agenda_salud.html', 
                             registros=registros, 
                             animales=animales, 
                             lotes=lotes, 
                             medicamentos=medicamentos)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para registrar esquema de vacunación
@app.route('/registrar-esquema-vacunacion', methods=['POST'])
def registrar_esquema():
    if 'conectado' in session:
        resultado = registrar_esquema_vacunacion(request.form)
        if resultado:
            flash('Esquema de vacunación registrado exitosamente.', 'success')
        else:
            flash('Error al registrar el esquema de vacunación.', 'error')
        return redirect(url_for('salud_tratamientos'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# API: Obtener alertas sanitarias para el dashboard
@app.route('/api/alertas-sanitarias', methods=['GET'])
def api_alertas_sanitarias():
    """
    Endpoint API que retorna un resumen de alertas sanitarias.
    
    Returns:
        JSON con estructura:
        {
            'total_alertas': int,
            'alta_urgencia': int,
            'media_urgencia': int,
            'baja_urgencia': int,
            'alertas_por_animal': [...]
        }
    """
    if 'conectado' in session:
        resumen = sql_obtener_resumen_alertas()
        return jsonify(resumen)
    else:
        return jsonify({'error': 'No autorizado'}), 401


# API: Obtener alertas para un animal específico
@app.route('/api/alertas-animal/<int:id_animal>', methods=['GET'])
def api_alertas_animal(id_animal):
    """
    Endpoint API que retorna las alertas sanitarias de un animal específico.
    
    Args:
        id_animal (int): ID del animal
    
    Returns:
        JSON con lista de alertas
    """
    if 'conectado' in session:
        alertas = sql_obtener_alertas_animal(id_animal)
        return jsonify({
            'id_animal': id_animal,
            'alertas': alertas,
            'total': len(alertas)
        })
    else:
        return jsonify({'error': 'No autorizado'}), 401


# ================================================================
# ENDPOINTS DE DESPARASITACIÓN Y VALIDACIÓN DE RETIRO (CRÍTICOS)
# ================================================================

@app.route('/api/validar-apto-venta/<int:id_animal>', methods=['GET'])
def api_validar_apto_venta(id_animal):
    """
    🚨 ENDPOINT CRÍTICO DE SEGURIDAD ALIMENTARIA 🚨
    
    Valida si un animal está apto para venta/sacrificio.
    Verifica periodos de retiro de medicamentos.
    
    Args:
        id_animal (int): ID del animal
    
    Returns:
        JSON: {
            'apto': bool,
            'mensaje': str (si no apto),
            'animal_id': int
        }
    
    Example:
        GET /api/validar-apto-venta/1
        Response: {"apto": false, "mensaje": "PELIGRO: Animal en retiro..."}
    """
    if 'conectado' in session:
        apto, mensaje = DesparasitacionService.validar_apto_consumo(id_animal, 'carne')
        
        return jsonify({
            'apto': apto,
            'mensaje': mensaje,
            'animal_id': id_animal,
            'tipo_validacion': 'venta'
        }), 200 if apto else 403
    else:
        return jsonify({'error': 'No autorizado'}), 401


@app.route('/api/validar-apto-ordeno/<int:id_animal>', methods=['GET'])
def api_validar_apto_ordeno(id_animal):
    """
    🚨 ENDPOINT CRÍTICO DE SEGURIDAD ALIMENTARIA 🚨
    
    Valida si un animal está apto para ordeño.
    Verifica periodos de retiro de medicamentos en leche.
    
    Args:
        id_animal (int): ID del animal
    
    Returns:
        JSON: {
            'apto': bool,
            'mensaje': str (si no apto),
            'animal_id': int
        }
    """
    if 'conectado' in session:
        apto, mensaje = DesparasitacionService.validar_apto_consumo(id_animal, 'leche')
        
        return jsonify({
            'apto': apto,
            'mensaje': mensaje,
            'animal_id': id_animal,
            'tipo_validacion': 'ordeno'
        }), 200 if apto else 403
    else:
        return jsonify({'error': 'No autorizado'}), 401


@app.route('/api/sugerencias-desparasitacion/<int:id_animal>', methods=['GET'])
def api_sugerencias_desparasitacion(id_animal):
    """
    Obtiene sugerencias de desparasitación para un animal.
    Basado en edad y estacionalidad.
    
    Args:
        id_animal (int): ID del animal
    
    Returns:
        JSON: {
            'animal_id': int,
            'sugerencias': List[Dict],
            'total': int
        }
    """
    if 'conectado' in session:
        sugerencias = DesparasitacionService.sugerir_desparasitacion(id_animal)
        
        return jsonify({
            'animal_id': id_animal,
            'sugerencias': sugerencias,
            'total': len(sugerencias)
        })
    else:
        return jsonify({'error': 'No autorizado'}), 401


@app.route('/api/animales-en-retiro', methods=['GET'])
def api_animales_en_retiro():
    """
    Obtiene lista de animales actualmente en periodo de retiro.
    
    Query Params:
        tipo: 'carne' o 'leche' (default: 'carne')
    
    Returns:
        JSON: {
            'animales_en_retiro': List[Dict],
            'total': int,
            'tipo_producto': str
        }
    """
    if 'conectado' in session:
        tipo_producto = request.args.get('tipo', 'carne')
        animales = DesparasitacionService.obtener_animales_en_retiro(tipo_producto)
        
        return jsonify({
            'animales_en_retiro': animales,
            'total': len(animales),
            'tipo_producto': tipo_producto
        })
    else:
        return jsonify({'error': 'No autorizado'}), 401


# ================================================================
# EJEMPLO DE ENDPOINT QUE USA VALIDACIÓN (Venta de Animal)
# ================================================================

@app.route('/vender-animal/<int:id_animal>', methods=['POST'])
def vender_animal(id_animal):
    """
    Ejemplo de endpoint que BLOQUEA la venta si el animal está en retiro.
    
    Este es un ejemplo de cómo integrar la validación de seguridad
    en cualquier proceso de venta.
    
    Args:
        id_animal (int): ID del animal a vender
    
    Returns:
        Redirect con mensaje de éxito o error
    """
    if 'conectado' in session:
        # 🚨 VALIDACIÓN CRÍTICA: Verificar periodo de retiro
        apto, mensaje = DesparasitacionService.validar_apto_consumo(id_animal, 'carne')
        
        if not apto:
            # BLOQUEAR VENTA - Animal en periodo de retiro
            flash(mensaje, 'error')
            return redirect(url_for('salud_tratamientos'))
        
        # Animal apto - Proceder con la venta
        # TODO: Implementar lógica de venta aquí
        # Por ejemplo:
        # - Registrar venta en tabla ventas
        # - Actualizar estado del animal
        # - Generar factura, etc.
        
        flash(f'Venta del animal #{id_animal} registrada exitosamente. Animal apto para consumo.', 'success')
        return redirect(url_for('salud_tratamientos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# ================================================================
# RUTAS PARA GESTIÓN DE INVENTARIO
# ================================================================

# Importar funciones de inventario
from controllers.funciones_inventario import (
    sql_lista_items,
    sql_obtener_item_por_id,
    sql_registrar_item,
    sql_actualizar_item,
    sql_eliminar_item,
    sql_estadisticas_inventario
)

# Ruta principal - Lista de items
@app.route('/inventario', methods=['GET'])
def inventario():
    """
    Muestra la lista de items del inventario con tabs por tipo.
    """
    if 'conectado' in session:
        # Obtener filtro de tipo si existe
        tipo_filtro = request.args.get('tipo')
        
        # Obtener items
        items = sql_lista_items(tipo_filtro)
        
        # Obtener estadísticas
        stats = sql_estadisticas_inventario()
        
        return render_template(
            'inventario/items_list.html',
            items=items,
            stats=stats,
            tipo_filtro=tipo_filtro
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para registrar nuevo item
@app.route('/inventario/registrar', methods=['POST'])
def registrar_item():
    """
    Procesa el formulario de registro de nuevo item.
    """
    if 'conectado' in session:
        resultado = sql_registrar_item(request.form)
        
        if resultado:
            flash('Item registrado exitosamente.', 'success')
        else:
            flash('Error al registrar el item.', 'error')
        
        return redirect(url_for('inventario'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para obtener item por ID (AJAX)
@app.route('/api/inventario/<int:id_item>', methods=['GET'])
def api_obtener_item(id_item):
    """
    API para obtener datos de un item específico.
    Usado para edición.
    """
    if 'conectado' in session:
        item = sql_obtener_item_por_id(id_item)
        
        if item:
            return jsonify(item)
        else:
            return jsonify({'error': 'Item no encontrado'}), 404
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Ruta para actualizar item
@app.route('/inventario/actualizar/<int:id_item>', methods=['POST'])
def actualizar_item(id_item):
    """
    Procesa el formulario de actualización de item.
    """
    if 'conectado' in session:
        resultado = sql_actualizar_item(id_item, request.form)
        
        if resultado:
            flash('Item actualizado exitosamente.', 'success')
        else:
            flash('Error al actualizar el item.', 'error')
        
        return redirect(url_for('inventario'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para eliminar item
@app.route('/inventario/eliminar/<int:id_item>', methods=['POST'])
def eliminar_item(id_item):
    """
    Elimina un item del inventario.
    """
    if 'conectado' in session:
        resultado = sql_eliminar_item(id_item)
        
        if resultado:
            flash('Item eliminado exitosamente.', 'success')
        else:
            flash('Error al eliminar el item.', 'error')
        
        return redirect(url_for('inventario'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para registrar salida de elemento
@app.route('/inventario/registrar-salida', methods=['POST'])
def registrar_salida():
    """
    Registra la salida de un elemento del inventario.
    Actualiza el stock y guarda el registro de salida.
    """
    if 'conectado' in session:
        try:
            id_item = int(request.form.get('id_item'))
            cantidad = float(request.form.get('cantidad'))
            fecha = request.form.get('fecha')
            motivo = request.form.get('motivo')
            responsable = request.form.get('responsable')
            observaciones = request.form.get('observaciones')
            
            # Obtener item actual
            item = sql_obtener_item_por_id(id_item)
            
            if not item:
                flash('Elemento no encontrado.', 'error')
                return redirect(url_for('inventario'))
            
            # Verificar que hay suficiente stock
            stock_actual = float(item['cantidad']) if item['cantidad'] is not None else 0.0
            
            if cantidad > stock_actual:
                flash(f'Stock insuficiente. Disponible: {stock_actual} {item["unidad_medida"]}', 'error')
                return redirect(url_for('inventario'))
            
            # Actualizar stock
            nuevo_stock = stock_actual - cantidad
            
            with connectionBD() as conexion:
                with conexion.cursor() as cursor:
                    # Actualizar cantidad en item
                    cursor.execute(
                        "UPDATE item SET cantidad = %s WHERE id_item = %s",
                        (nuevo_stock, id_item)
                    )
                    
                    # Registrar la salida en tabla de movimientos (si existe)
                    # Por ahora solo actualizamos el stock
                    # TODO: Mejorar con tabla movimiento_inventario
                    
                    conexion.commit()
            
            flash(f'Salida registrada exitosamente. Nuevo stock: {nuevo_stock} {item["unidad_medida"]}', 'success')
            
        except Exception as e:
            print(f"Error al registrar salida: {e}")
            flash('Error al registrar la salida.', 'error')
        
        return redirect(url_for('inventario'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para registrar entrada de elemento
@app.route('/inventario/registrar-entrada', methods=['POST'])
def registrar_entrada():
    """
    Registra la entrada de stock al inventario.
    Actualiza el stock y el costo unitario.
    """
    if 'conectado' in session:
        try:
            id_item = int(request.form.get('id_item'))
            cantidad = float(request.form.get('cantidad'))
            nuevo_costo = float(request.form.get('costo'))
            fecha = request.form.get('fecha')
            proveedor = request.form.get('proveedor')
            lote = request.form.get('lote')
            fecha_vencimiento = request.form.get('fecha_vencimiento') or None
            observaciones = request.form.get('observaciones')
            
            # Obtener item actual
            item = sql_obtener_item_por_id(id_item)
            
            if not item:
                flash('Elemento no encontrado.', 'error')
                return redirect(url_for('inventario'))
            
            # Actualizar stock
            stock_actual = float(item['cantidad']) if item['cantidad'] is not None else 0.0
            nuevo_stock = stock_actual + cantidad
            
            # Aquí actualizamos el costo directamente al nuevo costo ingresado
            # (Alternativamente se podría calcular un promedio ponderado)
            
            with connectionBD() as conexion:
                with conexion.cursor() as cursor:
                    # Actualizar cantidad y costo en item
                    cursor.execute(
                        """
                        UPDATE item 
                        SET cantidad = %s, costo = %s 
                        WHERE id_item = %s
                        """,
                        (nuevo_stock, nuevo_costo, id_item)
                    )
                    
                    # TODO: Guardar trazabilidad si implementamos tabla lotes/movimientos
                    
                    conexion.commit()
            
            flash(f'Entrada registrada exitosamente. Nuevo stock: {nuevo_stock} {item["unidad_medida"]}', 'success')
            
        except Exception as e:
            print(f"Error al registrar entrada: {e}")
            flash('Error al registrar la entrada.', 'error')
        
        return redirect(url_for('inventario'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# API para obtener lista de animales
@app.route('/api/animales-lista', methods=['GET'])
def api_animales_lista():
    """
    API para obtener lista simple de animales (para selects).
    """
    if 'conectado' in session:
        try:
            with connectionBD() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT id_animal, arete, nombre 
                        FROM animal 
                        WHERE estado = 'activo'
                        ORDER BY arete
                    """)
                    animales = cursor.fetchall()
            
            return jsonify(animales)
        except Exception as e:
            print(f"Error al obtener animales: {e}")
            return jsonify([]), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401
