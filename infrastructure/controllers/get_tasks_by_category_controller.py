from flask import Blueprint, request, jsonify
from application.usecases.get_tasks_by_category import GetTasksByCategoryUseCase
from infrastructure.repositories.task_repository import TaskRepository
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
get_tasks_by_category_blueprint = Blueprint('get_tasks_by_category', __name__)
repository = TaskRepository()
get_tasks_by_category_usecase = GetTasksByCategoryUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = ''


@get_tasks_by_category_blueprint.route('/tasks/category', methods=['GET'])
def get_tasks_by_category():
    category = request.args.get('category')
    if not category:
        return jsonify({"error": "La categoría es obligatoria"}), 400

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
            tasks = get_tasks_by_category_usecase.execute(user_id, category)
            # Comprobar si los elementos de tasks son diccionarios o necesitan ser convertidos
            if tasks and isinstance(tasks[0], dict):
                return jsonify(tasks), 200
            else:
                return jsonify([task.dict() for task in tasks]), 200
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
