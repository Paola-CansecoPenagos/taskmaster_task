from infrastructure.repositories.task_repository import TaskRepository

class DeleteTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: str, user_id: str):
        self.repository.delete_task(task_id, user_id)
