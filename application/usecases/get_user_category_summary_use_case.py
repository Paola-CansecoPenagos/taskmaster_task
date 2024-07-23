from infrastructure.repositories.task_repository import TaskRepository

class GetUserCategorySummaryUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, user_id: str):
        summary = self.repository.get_user_category_summary(user_id)
        progress_summary = self.repository.get_progress_summary(user_id)
        
        last_week_progress = progress_summary['last_week']
        if last_week_progress['total_tasks'] > 0:
            last_week_rate = (last_week_progress['tasks_completed'] / last_week_progress['total_tasks']) * 100
        else:
            last_week_rate = 0

        current_week_progress = progress_summary['current_week']
        if current_week_progress['total_tasks'] > 0:
            current_week_rate = (current_week_progress['tasks_completed'] / current_week_progress['total_tasks']) * 100
        else:
            current_week_rate = 0

        if current_week_progress['total_tasks'] > 0:
            progress_of_current_tasks = (current_week_progress['tasks_in_progress'] / current_week_progress['total_tasks']) * 100
        else:
            progress_of_current_tasks = 0

        predicted_completion_rate = (last_week_rate + progress_of_current_tasks) / 2

        trend = "positive" if last_week_rate > 50 else "negative" if last_week_rate < 50 else "neutral"
        
        summary.update({
            "weekly_progress": progress_summary,
            "last_week_rate": last_week_rate,
            "current_week_rate": current_week_rate,
            "predicted_completion_rate": predicted_completion_rate,
            "trend": trend
        })
        return summary
