from infrastructure.repositories.task_repository import TaskRepository

class GetTasksByCategoryUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, user_id: str, category: str):
        tasks = self.repository.get_tasks_by_category(user_id, category)
        return tasks
