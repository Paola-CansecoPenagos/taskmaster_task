from flask import Blueprint, request, jsonify
from application.usecases.create_task import CreateTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
from utils.text_utils import escape_html, escape_javascript, trim_text
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración del Blueprint
create_task_blueprint = Blueprint('create_task', __name__)
repository = TaskRepository()
create_task_usecase = CreateTaskUseCase(repository=repository)

# Clave secreta para decodificar el JWT (debería estar en un archivo de configuración o variable de entorno)
SECRET_KEY = ''

@create_task_blueprint.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
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
        task_data = data.copy()
        task_data['user_id'] = user_id

        # Sanitizar y validar datos
        task_data['title'] = escape_html(task_data.get('title', ''))
        task_data['description'] = escape_html(task_data.get('description', ''))

        task_data['title'] = escape_javascript(task_data['title'])
        task_data['description'] = escape_javascript(task_data['description'])

        task_data['title'] = trim_text(task_data['title'])
        task_data['description'] = trim_text(task_data['description'])

        try:
            result = create_task_usecase.execute(task_data)
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": "Error de validación: " + str(e)}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
