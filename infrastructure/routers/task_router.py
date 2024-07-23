from flask import Blueprint
from infrastructure.controllers.create_task_controller import create_task_blueprint
from infrastructure.controllers.edit_task_controller import edit_task_blueprint
from infrastructure.controllers.complete_subtask_controller import complete_subtask_blueprint
from infrastructure.controllers.get_tasks_controller import get_tasks_by_user_blueprint
from infrastructure.controllers.get_task_controller import get_task_by_id_blueprint
from infrastructure.controllers.get_tasks_by_category_controller import get_tasks_by_category_blueprint
from infrastructure.controllers.get_tasks_by_progress_controller import get_tasks_by_progress_blueprint
from infrastructure.controllers.user_category_summary_controller import user_category_summary_blueprint
from infrastructure.controllers.delete_task_controller import delete_task_blueprint

task_router = Blueprint('task_router', __name__)

task_router.register_blueprint(get_tasks_by_user_blueprint, url_prefix='/')
task_router.register_blueprint(get_task_by_id_blueprint, url_prefix='/')
task_router.register_blueprint(create_task_blueprint, url_prefix='/')
task_router.register_blueprint(edit_task_blueprint, url_prefix='/')
task_router.register_blueprint(complete_subtask_blueprint, url_prefix='/')
task_router.register_blueprint(get_tasks_by_category_blueprint, url_prefix='/')
task_router.register_blueprint(get_tasks_by_progress_blueprint, url_prefix='/')
task_router.register_blueprint(user_category_summary_blueprint, url_prefix='/')
task_router.register_blueprint(delete_task_blueprint, url_prefix='/')
