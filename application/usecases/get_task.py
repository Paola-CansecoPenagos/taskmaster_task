from domain.entities.task import Task
from infrastructure.repositories.task_repository import TaskRepository

class GetTaskByIdUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: str):
        task = self.repository.find_task_by_id(task_id)
        if task is None:
            raise ValueError("Tarea no encontrada.")
        return task
