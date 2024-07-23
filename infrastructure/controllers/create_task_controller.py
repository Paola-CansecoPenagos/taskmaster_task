from flask import Blueprint, request, jsonify
from application.usecases.create_task import CreateTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
from utils.text_utils import escape_html, escape_javascript, trim_text
from infrastructure.services.rabbitmq_producer import send_verification_request
import threading
from threading import Condition

create_task_blueprint = Blueprint('create_task', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
create_task_usecase = CreateTaskUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result  
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)  
        condition.notify()  

@create_task_blueprint.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    user_token = request.headers.get('Authorization', '').split(' ')[1]

    with condition:
        thread = threading.Thread(target=send_verification_request, args=(
            user_token, 
            'response_queue', 
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=10)  # Espera a que la verificación se complete o expire el tiempo

    if verification_result.get('exists', False) and 'user_id' in verification_result:
        task_data = data.copy()
        task_data['user_id'] = verification_result['user_id']

        task_data['title'] = escape_html(task_data['title'])
        task_data['description'] = escape_html(task_data['description'])

        task_data['title'] = escape_javascript(task_data['title'])
        task_data['description'] = escape_javascript(task_data['description'])

        task_data['title'] = trim_text(task_data['title'])
        task_data['description'] = trim_text(task_data['description'])

        try:
            result = create_task_usecase.execute(task_data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": "Error de validación: " + str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
