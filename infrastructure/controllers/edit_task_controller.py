from flask import Blueprint, request, jsonify
from application.usecases.edit_task import EditTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
from utils.text_utils import escape_html, escape_javascript, trim_text
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

edit_task_blueprint = Blueprint('edit_task', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
edit_task_usecase = EditTaskUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@edit_task_blueprint.route('/<task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    user_token = request.headers.get('Authorization', '').split(' ')[1]

    data['title'] = escape_html(data['title'])
    data['description'] = escape_html(data['description'])

    data['title'] = escape_javascript(data['title'])
    data['description'] = escape_javascript(data['description'])

    data['title'] = trim_text(data['title'])
    data['description'] = trim_text(data['description'])

    with condition:
        thread = threading.Thread(target=send_verification_request, args=(
            user_token,
            'response_queue', 
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=10)

    if verification_result.get('exists', False) and verification_result['user_id']:
        data['user_id'] = verification_result['user_id']  # Agregar user_id a los datos de la tarea
        try:
            result = edit_task_usecase.execute(task_id, data)
            return jsonify({"message": "Tarea actualizada exitosamente"}), 200
        except ValueError as e:
            return jsonify({"error": "La actualización de la tarea falló debido a una entrada inválida: " + str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
