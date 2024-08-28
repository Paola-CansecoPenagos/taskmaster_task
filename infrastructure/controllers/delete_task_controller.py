from flask import Blueprint, request, jsonify
from application.usecases.delete_task import DeleteTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
delete_task_blueprint = Blueprint('delete_task', __name__)
repository = TaskRepository()
delete_task_usecase = DeleteTaskUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = ''


@delete_task_blueprint.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
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

    if user_id:
        try:
            delete_task_usecase.execute(task_id, user_id)
            return jsonify({"message": "Tarea eliminada exitosamente"}), 200
        except ValueError as e:
            return jsonify({"error": "Error de validación: " + str(e)}), 403
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
