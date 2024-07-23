from flask import Blueprint, request, jsonify
from application.usecases.complete_subtask import UpdateSubtasksUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

complete_subtask_blueprint = Blueprint('complete_subtask', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
update_subtasks_usecase = UpdateSubtasksUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@complete_subtask_blueprint.route('/<task_id>/subtasks', methods=['PATCH'])
def update_subtasks(task_id):
    data = request.get_json()
    subtasks = data.get('subtasks', [])
    user_token = request.headers.get('Authorization', '').split(' ')[1]  # Obtener el token JWT del encabezado

    with condition:

        thread = threading.Thread(target=send_verification_request, args=(
            user_token,
            'response_queue',  
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=10)  

    if verification_result.get('exists', False) and verification_result['user_id']:
        try:
            result = update_subtasks_usecase.execute(task_id, subtasks)
            return jsonify({"message": "Subtareas actualizadas exitosamente", "progress": result['progress']}), 200
        except ValueError as e:
            return jsonify({"error": "Error de validación: " + str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Ocurrió un error inesperado: " + str(e)}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404