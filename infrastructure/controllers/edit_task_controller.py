from flask import Blueprint, request, jsonify
from application.usecases.edit_task import EditTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
from utils.text_utils import escape_html, escape_javascript, trim_text
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
edit_task_blueprint = Blueprint('edit_task', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
edit_task_usecase = EditTaskUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = '6f8632261860cdc4a6aed3683dbf12093202b6ad3fa9dc8dec427c752002a82b'


@edit_task_blueprint.route('/<task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    user_token = request.headers.get('Authorization', '').split(' ')[1]

    # Sanitización y escape de los datos de la tarea
    data['title'] = escape_html(data.get('title', ''))
    data['description'] = escape_html(data.get('description', ''))

    data['title'] = escape_javascript(data['title'])
    data['description'] = escape_javascript(data['description'])

    data['title'] = trim_text(data['title'])
    data['description'] = trim_text(data['description'])

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
        data['user_id'] = user_id  # Agregar user_id a los datos de la tarea
        try:
            result = edit_task_usecase.execute(task_id, data)
            return jsonify({"message": "Tarea actualizada exitosamente"}), 200
        except ValueError as e:
            return jsonify({"error": "La actualización de la tarea falló debido a una entrada inválida: " + str(e)}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
