from flask import Blueprint, request, jsonify
from application.usecases.complete_subtask import UpdateSubtasksUseCase
from infrastructure.repositories.task_repository import TaskRepository
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
complete_subtask_blueprint = Blueprint('complete_subtask', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='')
update_subtasks_usecase = UpdateSubtasksUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = '6f8632261860cdc4a6aed3683dbf12093202b6ad3fa9dc8dec427c752002a82b'

@complete_subtask_blueprint.route('/<task_id>/subtasks', methods=['PATCH'])
def update_subtasks(task_id):
    data = request.get_json()
    subtasks = data.get('subtasks', [])
    user_token = request.headers.get('Authorization', '').split(' ')[1]

    try:
        # Decodificar el JWT
        decoded_token = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    except InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except Exception as e:
        print(f"Error al decodificar el token: {str(e)}")
        return jsonify({"error": "Error al procesar el token"}), 400

    if user_id:
        try:
            result = update_subtasks_usecase.execute(task_id, subtasks)
            return jsonify({"message": "Subtareas actualizadas exitosamente", "progress": result['progress']}), 200
        except ValueError as e:
            return jsonify({"error": "Error de validación: " + str(e)}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
