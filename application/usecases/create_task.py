from domain.entities.task import Task, Subtask
from domain.validations.text_validations import validate_text_length
from domain.validations.date_validations import validate_start_reminder_date, validate_due_date, validate_date_order
from domain.validations.time_validations import validate_time_order
from domain.validations.subtask_validations import validate_subtasks
from domain.validations.priority_validations import validate_priority
from domain.validations.blacklisting_validations import validate_text
from domain.validations.type_validations import validate_type
from domain.validations.offensive_validations import validate_offensive_content
from infrastructure.repositories.task_repository import TaskRepository
from typing import List

class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def calculate_progress(self, subtasks: List[Subtask]) -> int:
        if not subtasks:
            return 0
        completed_subtasks = sum(1 for subtask in subtasks if subtask.completed)
        return int((completed_subtasks / len(subtasks)) * 100)

    def execute(self, task_data):
        validate_text_length(task_data['title'], 3, 50, "El título")
        validate_text_length(task_data['description'], 3, 500, "La descripción")

        validate_offensive_content(task_data['title'], "El título")
        validate_offensive_content(task_data['description'], "La descripción")
        validate_subtasks(task_data['subtasks'])
        
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

        task_data['progress'] = self.calculate_progress(subtasks)

        tasks = []
        user_ids = task_data.get('user_ids', [])
        if task_data['type'] == 'grupal':
            user_ids.append(task_data['user_id'])
        elif task_data['type'] == 'asignar':
            user_ids = [uid for uid in user_ids if uid != task_data['user_id']]
        else:
            user_ids = [task_data['user_id']]

        for uid in user_ids:
            task = Task(
                user_id=uid,
                title=task_data['title'],
                description=task_data['description'],
                category=task_data['category'],
                priority=task_data['priority'],
                start_reminder_date=task_data['start_reminder_date'],
                due_date=task_data['due_date'],
                due_time=task_data['due_time'],
                start_reminder_time=task_data['start_reminder_time'],
                end_reminder_time=task_data['end_reminder_time'],
                subtasks=subtasks,
                type=task_data['type'],
                progress=task_data['progress']
            )
            tasks.append(task)

        for task in tasks:
            self.repository.add_task(task)

        return {"message": "Tareas creadas exitosamente"}