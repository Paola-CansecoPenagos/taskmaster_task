from flask import Blueprint, request, jsonify
from application.usecases.get_tasks import GetTasksByUserUseCase
from infrastructure.repositories.task_repository import TaskRepository
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
get_tasks_by_user_blueprint = Blueprint('get_tasks_by_user', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
get_tasks_by_user_usecase = GetTasksByUserUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = '6f8632261860cdc4a6aed3683dbf12093202b6ad3fa9dc8dec427c752002a82b'

@get_tasks_by_user_blueprint.route('/tasks', methods=['GET'])
def get_tasks_by_user():
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

    # Verificación de la existencia del usuario y obtención de las tareas
    try:
        tasks = get_tasks_by_user_usecase.execute(user_id)
        # Comprobar si los elementos de tasks son diccionarios o necesitan ser convertidos
        if tasks and isinstance(tasks[0], dict):
            return jsonify(tasks), 200
        else:
            return jsonify([task.dict() for task in tasks]), 200
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({"error": "Ocurrió un error inesperado"}), 500
