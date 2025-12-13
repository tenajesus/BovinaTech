from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.funciones_alimentacion import *
from controllers.funciones_inventario import sql_lista_items

alimentacion = Blueprint('alimentacion', __name__)

@alimentacion.route('/alimentacion')
def index():
    return redirect(url_for('alimentacion.registro_diario'))

# --- FÓRMULAS ---

@alimentacion.route('/alimentacion/formulas', methods=['GET', 'POST'])
def formulas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        
        # Procesar ingredientes (se asume que vienen como listas paralelas o JSON)
        # Simplificación: recibimos listas de ids y porcentajes
        ids_items = request.form.getlist('id_item[]')
        porcentajes = request.form.getlist('porcentaje[]')
        
        ingredientes = []
        for i in range(len(ids_items)):
            if ids_items[i] and porcentajes[i]:
                ingredientes.append({
                    'id_item': int(ids_items[i]),
                    'porcentaje': float(porcentajes[i])
                })
        
        if sql_crear_formula(nombre, descripcion, costo, ingredientes):
            flash('Fórmula creada exitosamente', 'success')
        else:
            flash('Error al crear fórmula', 'error')
            
        return redirect(url_for('alimentacion.formulas'))
        
    formulas = sql_obtener_formulas()
    # Obtener items de tipo 'alimento' para el selector de ingredientes
    items_alimento = [i for i in sql_lista_items() if i['tipo'] == 'alimento']
    
    return render_template('alimentacion/formulas_list.html', formulas=formulas, items=items_alimento)

@alimentacion.route('/alimentacion/formulas/editar/<int:id>', methods=['POST'])
def editar_formula(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    
    ids_items = request.form.getlist('id_item[]')
    porcentajes = request.form.getlist('porcentaje[]')
    
    ingredientes = []
    for i in range(len(ids_items)):
        if ids_items[i] and porcentajes[i]:
            ingredientes.append({
                'id_item': int(ids_items[i]),
                'porcentaje': float(porcentajes[i])
            })
            
    if sql_editar_formula(id, nombre, descripcion, costo, ingredientes):
        flash('Fórmula actualizada', 'success')
    else:
        flash('Error al actualizar', 'error')
        
    return redirect(url_for('alimentacion.formulas'))

# --- REGISTRO DIARIO ---

@alimentacion.route('/alimentacion/registro-diario', methods=['GET', 'POST'])
def registro_diario():
    if request.method == 'POST':
        fecha = request.form['fecha']
        id_lote = request.form['id_lote']
        id_formula = request.form['id_formula']
        
        # Procesar datos de la tabla dinámica
        # Se espera que el form envíe arrays con datos de cada animal
        ids_animales = request.form.getlist('id_animal[]')
        raciones_asignadas = request.form.getlist('racion_asignada[]')
        raciones_consumidas = request.form.getlist('racion_consumida[]')
        comentarios_list = request.form.getlist('comentarios[]')
        
        registros = []
        for i in range(len(ids_animales)):
            registros.append({
                'id_animal': int(ids_animales[i]),
                'racion_asignada': float(raciones_asignadas[i] or 0),
                'racion_consumida': float(raciones_consumidas[i] or 0),
                'comentarios': comentarios_list[i]
            })
            
        if sql_registrar_alimentacion_diaria(fecha, id_lote, id_formula, registros):
            flash('Registro diario guardado exitosamente', 'success')
        else:
            flash('Error al guardar registro', 'error')
            
        return redirect(url_for('alimentacion.registro_diario'))

    # GET: Cargar datos iniciales
    formulas = sql_obtener_formulas()
    lotes = sql_obtener_lotes()
        
    return render_template('alimentacion/registro_diario.html', formulas=formulas, lotes=lotes)

# API para obtener animales de un lote (AJAX)
@alimentacion.route('/api/lotes/<int:id_lote>/animales')
def api_animales_lote(id_lote):
    animales = sql_obtener_animales_por_lote(id_lote)
    return jsonify(animales)
