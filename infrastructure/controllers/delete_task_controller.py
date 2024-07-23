from flask import Blueprint, request, jsonify
from application.usecases.delete_task import DeleteTaskUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

delete_task_blueprint = Blueprint('delete_task', __name__)
repository = TaskRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterTask')
delete_task_usecase = DeleteTaskUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@delete_task_blueprint.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
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
            delete_task_usecase.execute(task_id, verification_result['user_id'])
            return jsonify({"message": "Tarea eliminada exitosamente"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
