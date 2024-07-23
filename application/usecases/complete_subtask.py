from infrastructure.repositories.task_repository import TaskRepository

class UpdateSubtasksUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def calculate_progress(self, subtasks):
        if not subtasks:
            return 0
        completed_subtasks = sum(1 for subtask in subtasks if subtask.completed)
        return int((completed_subtasks / len(subtasks)) * 100)

    def execute(self, task_id, subtasks_data):
        task = self.repository.find_task_by_id(task_id)
        if not task:
            raise ValueError("Tarea no encontrada")
        
        for subtask_data in subtasks_data:
            for subtask in task.subtasks:
                if subtask.title == subtask_data['title']:
                    subtask.completed = subtask_data['completed']

        task.progress = self.calculate_progress(task.subtasks)
        self.repository.update_task(task_id, task)  # Aquí se pasa la instancia de Task
        return {'progress': task.progress}
