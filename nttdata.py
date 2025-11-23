from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de datos simulada en memoria
empleados = [
    {
        'id': 1,
        'nombre': 'María García',
        'cargo': 'Desarrolladora Senior',
        'departamento': 'IT',
        'email': 'maria.garcia@nttdata.com'
    },
    {
        'id': 2,
        'nombre': 'Carlos López',
        'cargo': 'Project Manager',
        'departamento': 'PMO',
        'email': 'carlos.lopez@nttdata.com'
    },
    {
        'id': 3,
        'nombre': 'Ana Martínez',
        'cargo': 'Arquitecta de Software',
        'departamento': 'IT',
        'email': 'ana.martinez@nttdata.com'
    }
]

proyectos = [
    {
        'id': 1,
        'nombre': 'Transformación Digital Banco XYZ',
        'cliente': 'Banco XYZ',
        'estado': 'En progreso',
        'empleadosAsignados': [1, 2]
    },
    {
        'id': 2,
        'nombre': 'Migración Cloud Retail SA',
        'cliente': 'Retail SA',
        'estado': 'Planificación',
        'empleadosAsignados': [3]
    }
]

# ==================== ENDPOINTS DE EMPLEADOS ====================

@app.route('/api/empleados', methods=['GET'])
def obtener_empleados():
    """Obtener todos los empleados"""
    return jsonify({
        'success': True,
        'data': empleados,
        'total': len(empleados)
    }), 200

@app.route('/api/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    """Obtener empleado por ID"""
    empleado = next((e for e in empleados if e['id'] == id), None)
    if not empleado:
        return jsonify({'success': False, 'message': 'Empleado no encontrado'}), 404
    return jsonify({'success': True, 'data': empleado}), 200

@app.route('/api/empleados', methods=['POST'])
def crear_empleado():
    """Crear nuevo empleado"""
    data = request.get_json()
    
    if not all(key in data for key in ['nombre', 'cargo', 'departamento', 'email']):
        return jsonify({
            'success': False,
            'message': 'Todos los campos son requeridos'
        }), 400
    
    nuevo_empleado = {
        'id': len(empleados) + 1,
        'nombre': data['nombre'],
        'cargo': data['cargo'],
        'departamento': data['departamento'],
        'email': data['email']
    }
    
    empleados.append(nuevo_empleado)
    return jsonify({'success': True, 'data': nuevo_empleado}), 201

@app.route('/api/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    """Actualizar empleado"""
    empleado = next((e for e in empleados if e['id'] == id), None)
    if not empleado:
        return jsonify({'success': False, 'message': 'Empleado no encontrado'}), 404
    
    data = request.get_json()
    if 'nombre' in data:
        empleado['nombre'] = data['nombre']
    if 'cargo' in data:
        empleado['cargo'] = data['cargo']
    if 'departamento' in data:
        empleado['departamento'] = data['departamento']
    if 'email' in data:
        empleado['email'] = data['email']
    
    return jsonify({'success': True, 'data': empleado}), 200

@app.route('/api/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    """Eliminar empleado"""
    global empleados
    empleado = next((e for e in empleados if e['id'] == id), None)
    if not empleado:
        return jsonify({'success': False, 'message': 'Empleado no encontrado'}), 404
    
    empleados = [e for e in empleados if e['id'] != id]
    return jsonify({'success': True, 'message': 'Empleado eliminado correctamente'}), 200

# ==================== ENDPOINTS DE PROYECTOS ====================

@app.route('/api/proyectos', methods=['GET'])
def obtener_proyectos():
    """Obtener todos los proyectos"""
    return jsonify({
        'success': True,
        'data': proyectos,
        'total': len(proyectos)
    }), 200

@app.route('/api/proyectos/<int:id>', methods=['GET'])
def obtener_proyecto(id):
    """Obtener proyecto por ID"""
    proyecto = next((p for p in proyectos if p['id'] == id), None)
    if not proyecto:
        return jsonify({'success': False, 'message': 'Proyecto no encontrado'}), 404
    return jsonify({'success': True, 'data': proyecto}), 200

@app.route('/api/proyectos', methods=['POST'])
def crear_proyecto():
    """Crear nuevo proyecto"""
    data = request.get_json()
    
    if not all(key in data for key in ['nombre', 'cliente']):
        return jsonify({
            'success': False,
            'message': 'Nombre y cliente son requeridos'
        }), 400
    
    nuevo_proyecto = {
        'id': len(proyectos) + 1,
        'nombre': data['nombre'],
        'cliente': data['cliente'],
        'estado': data.get('estado', 'Planificación'),
        'empleadosAsignados': data.get('empleadosAsignados', [])
    }
    
    proyectos.append(nuevo_proyecto)
    return jsonify({'success': True, 'data': nuevo_proyecto}), 201

@app.route('/api/proyectos/<int:id>/asignar', methods=['POST'])
def asignar_empleado(id):
    """Asignar empleado a proyecto"""
    proyecto = next((p for p in proyectos if p['id'] == id), None)
    if not proyecto:
        return jsonify({'success': False, 'message': 'Proyecto no encontrado'}), 404
    
    data = request.get_json()
    empleado_id = data.get('empleadoId')
    
    empleado = next((e for e in empleados if e['id'] == empleado_id), None)
    if not empleado:
        return jsonify({'success': False, 'message': 'Empleado no encontrado'}), 404
    
    if empleado_id not in proyecto['empleadosAsignados']:
        proyecto['empleadosAsignados'].append(empleado_id)
    
    return jsonify({'success': True, 'data': proyecto}), 200

@app.route('/api/proyectos/<int:id>/empleados', methods=['GET'])
def obtener_empleados_proyecto(id):
    """Obtener empleados de un proyecto"""
    proyecto = next((p for p in proyectos if p['id'] == id), None)
    if not proyecto:
        return jsonify({'success': False, 'message': 'Proyecto no encontrado'}), 404
    
    empleados_del_proyecto = [
        e for e in empleados if e['id'] in proyecto['empleadosAsignados']
    ]
    
    return jsonify({'success': True, 'data': empleados_del_proyecto}), 200

# ==================== ENDPOINT DE INICIO ====================

@app.route('/', methods=['GET'])
def inicio():
    """Endpoint de inicio"""
    return jsonify({
        'message': 'API NTT Data - Sistema de Gestión de Proyectos',
        'version': '1.0.0',
        'endpoints': {
            'empleados': '/api/empleados',
            'proyectos': '/api/proyectos'
        }
    }), 200

# Manejo de errores
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'success': False, 'message': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def error_servidor(error):
    return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print('🚀 API NTT Data ejecutándose en http://localhost:5000')
    print('📊 Endpoints disponibles:')
    print('   GET    /api/empleados')
    print('   POST   /api/empleados')
    print('   GET    /api/proyectos')
    print('   POST   /api/proyectos')
    app.run(debug=True, host='0.0.0.0', port=5000)