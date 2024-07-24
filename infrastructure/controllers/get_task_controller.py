from flask import Blueprint, request, jsonify
from application.usecases.get_task import GetTaskByIdUseCase
from infrastructure.repositories.task_repository import TaskRepository
from jwt.exceptions import InvalidTokenError, DecodeError
import jwt

# Configuración del Blueprint
get_task_by_id_blueprint = Blueprint('get_task_by_id', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
get_task_by_id_usecase = GetTaskByIdUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = '6f8632261860cdc4a6aed3683dbf12093202b6ad3fa9dc8dec427c752002a82b'

@get_task_by_id_blueprint.route('/task/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    user_token = request.headers.get('Authorization', '').split(' ')[1]  # Obtener el token JWT del encabezado

    try:
        # Decodificar el JWT
        decoded_token = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    except InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except Exception as e:
        print(f"Error al decodificar el token: {str(e)}")
        return jsonify({"error": "Error al procesar el token"}), 400

    # Verificar la existencia del usuario y obtener la tarea
    try:
        task = get_task_by_id_usecase.execute(task_id)
        if task.user_id == user_id:  # Verificar que la tarea pertenezca al usuario
            return jsonify(task.dict()), 200
        else:
            return jsonify({"error": "Acceso denegado"}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
