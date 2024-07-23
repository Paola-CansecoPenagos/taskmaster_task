from domain.entities.task import Task, Subtask
from typing import List
from domain.validations.text_validations import validate_text_length
from domain.validations.date_validations import validate_start_reminder_date, validate_due_date, validate_date_order
from domain.validations.time_validations import validate_time_order
from domain.validations.subtask_validations import validate_subtasks
from domain.validations.priority_validations import validate_priority
from domain.validations.blacklisting_validations import validate_text
from domain.validations.offensive_validations import validate_offensive_content
from domain.validations.type_validations import validate_type
from infrastructure.repositories.task_repository import TaskRepository

class EditTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def calculate_progress(self, subtasks: List[Subtask]) -> int:
        if not subtasks:
            return 0
        completed_subtasks = sum(1 for subtask in subtasks if subtask.completed)
        return int((completed_subtasks / len(subtasks)) * 100)

    def execute(self, task_id, task_data):
        validate_text_length(task_data['title'], 3, 50, "El título")
        validate_text_length(task_data['description'], 3, 500, "La descripción")

        validate_offensive_content(task_data['title'], "El título")
        validate_offensive_content(task_data['description'], "La descripción")

        if isinstance(task_data['subtasks'], list):
            subtasks = [Subtask(**subtask) for subtask in task_data['subtasks']]
            for subtask in subtasks:
                validate_offensive_content(subtask.title,"El texto de la subtarea contiene mensajes ofensivos")
        else:
            raise ValueError("Las subtareas deben ser una lista de diccionarios.")
            
        validate_start_reminder_date(task_data['start_reminder_date'])
        validate_due_date(task_data['due_date'])
        validate_date_order(task_data['start_reminder_date'], task_data['due_date'])
        validate_time_order(task_data['start_reminder_time'], task_data['end_reminder_time'])

        validate_priority(task_data['priority'])
        validate_type(task_data['type'])

        validate_text(task_data['title'], "El título")
        validate_text(task_data['description'], "La descripción")

        subtasks = [Subtask(**subtask) for subtask in task_data['subtasks']]
        task_data['progress'] = self.calculate_progress(subtasks)
        task_data['subtasks'] = subtasks  # Asegúrate de incluir subtasks en task_data
        task = Task(**task_data)  # Asegúrate de que user_id esté presente en task_data
        return self.repository.update_task(task_id, task)
