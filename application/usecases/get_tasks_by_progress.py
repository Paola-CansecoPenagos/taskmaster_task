from infrastructure.repositories.task_repository import TaskRepository

class GetTasksByProgressUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, user_id: str, progress_status: str):
        tasks = self.repository.get_tasks_by_progress(user_id, progress_status)
        return tasks
