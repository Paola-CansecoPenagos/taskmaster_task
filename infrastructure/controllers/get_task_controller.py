from flask import Blueprint, request, jsonify
from application.usecases.get_task import GetTaskByIdUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

get_task_by_id_blueprint = Blueprint('get_task_by_id', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
get_task_by_id_usecase = GetTaskByIdUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@get_task_by_id_blueprint.route('/task/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    user_token = request.headers.get('Authorization', '').split(' ')[1]  # Obtener el token JWT del encabezado

    with condition:
        # Envío de la solicitud de verificación del usuario
        thread = threading.Thread(target=send_verification_request, args=(
            user_token,
            'response_queue',  # Una cola única para esta operación
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=10)  # Espera a que se complete la verificación o se agote el tiempo

    # Verificación de la existencia del usuario
    if verification_result.get('exists', False) and verification_result['user_id']:
        try:
            task = get_task_by_id_usecase.execute(task_id)
            if task.user_id == verification_result['user_id']:  # Verificar que la tarea pertenezca al usuario
                return jsonify(task.dict()), 200
            else:
                return jsonify({"error": "Acceso denegado"}), 403
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
