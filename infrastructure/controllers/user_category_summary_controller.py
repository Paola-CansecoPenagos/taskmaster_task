from flask import Blueprint, request, jsonify
from application.usecases.get_user_category_summary_use_case import GetUserCategorySummaryUseCase
from infrastructure.repositories.task_repository import TaskRepository
from infrastructure.services.rabbitmq_producer import send_verification_request
from threading import Condition
import threading

user_category_summary_blueprint = Blueprint('user_category_summary', __name__)
repository = TaskRepository()
use_case = GetUserCategorySummaryUseCase(repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    global verification_result
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id', None)
        condition.notify()

@user_category_summary_blueprint.route('/categories/summary', methods=['GET'])
def get_user_category_summary():
    user_token = request.headers.get('Authorization', '').split(' ')[1]  

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
            summary = use_case.execute(verification_result['user_id'])
            return jsonify(summary), 200
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
