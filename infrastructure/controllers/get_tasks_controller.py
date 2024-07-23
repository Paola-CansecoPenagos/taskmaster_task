from flask import Blueprint, request, jsonify
from application.usecases.get_tasks import GetTasksByUserUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

get_tasks_by_user_blueprint = Blueprint('get_tasks_by_user', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
get_tasks_by_user_usecase = GetTasksByUserUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@get_tasks_by_user_blueprint.route('/tasks', methods=['GET'])
def get_tasks_by_user():
    user_token = request.headers.get('Authorization', '').split(' ')[1]  # Obtener el token JWT del encabezado

    with condition:
        # Envío de la solicitud de verificación del usuario
        thread = threading.Thread(target=send_verification_request, args=(
            user_token,
            'response_queue',  # Una cola única para esta operación
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=20)  # Espera a que se complete la verificación o se agote el tiempo

    # Verificación de la existencia del usuario
    if verification_result.get('exists', False) and verification_result['user_id']:
        try:
            tasks = get_tasks_by_user_usecase.execute(verification_result['user_id'])
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
