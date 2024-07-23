from flask import Blueprint, request, jsonify
from application.usecases.get_tasks_by_progress import GetTasksByProgressUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

get_tasks_by_progress_blueprint = Blueprint('get_tasks_by_progress', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
get_tasks_by_progress_usecase = GetTasksByProgressUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@get_tasks_by_progress_blueprint.route('/tasks/progress', methods=['GET'])
def get_tasks_by_progress():
    progress_status = request.args.get('progress_status')
    if not progress_status:
        return jsonify({"error": "El estado de progreso es obligatorio"}), 400

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
            tasks = get_tasks_by_progress_usecase.execute(verification_result['user_id'], progress_status)
            if tasks and isinstance(tasks[0], dict):
                return jsonify(tasks), 200
            else:
                return jsonify([task.dict() for task in tasks]), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
