from infrastructure.repositories.task_repository import TaskRepository

class GetTasksByUserUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, user_id: str):
        tasks = self.repository.get_tasks_by_user(user_id)
        return tasks
