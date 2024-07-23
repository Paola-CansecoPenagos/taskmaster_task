from pymongo import MongoClient
from bson import ObjectId
from domain.entities.task import Task
from typing import List
from collections import defaultdict
from datetime import datetime, timedelta

class TaskRepository:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db['tasks']
    
    def find_task_by_title(self, user_id: str, title: str):
        task_data = self.collection.find_one({"user_id": user_id, "title": title})
        if task_data:
            return Task(**task_data)
        return None
    
    def add_task(self, task: Task):
        if self.find_task_by_title(task.user_id, task.title):
            raise Exception("Ya existe una tarea con el mismo título para este usuario.")
        
        task_dict = task.dict()
        task_dict['subtasks'] = [subtask.dict() for subtask in task.subtasks]
        return self.collection.insert_one(task_dict)
    
    def find_task_by_id(self, task_id: str):
        try:
            object_id = ObjectId(task_id)
            task_data = self.collection.find_one({"_id": object_id})
            if task_data:
                return Task(**task_data)  # Convierte el dict a una instancia de Task
            return None
        except Exception as e:
            print(f"Error al convertir task_id a ObjectId: {e}")
            return None

    def update_task(self, task_id: str, task: Task):
        try:
            object_id = ObjectId(task_id)
            task_data = task.dict()  # Convierte Task a dict
            task_data['subtasks'] = [subtask.dict() for subtask in task.subtasks]  # Convierte cada subtask a dict
            self.collection.update_one({"_id": object_id}, {"$set": task_data})
        except Exception as e:
            print(f"Error al actualizar tarea: {e}")

    def get_tasks_by_user(self, user_id: str) -> List[dict]:
        projection = {"_id": 1, "title": 1, "progress": 1}
        tasks_data = self.collection.find({"user_id": user_id}, projection)
        return [{"id": str(task["_id"]), "title": task["title"], "progress": task["progress"]} for task in tasks_data]
    
    def get_tasks_by_category(self, user_id: str, category: str) -> List[dict]:
        projection = {"_id": 1, "title": 1, "progress": 1}
        tasks_data = self.collection.find({"user_id": user_id, "category": category}, projection)
        return [{"id": str(task["_id"]), "title": task["title"], "progress": task["progress"]} for task in tasks_data]

    def get_tasks_by_progress(self, user_id: str, progress_status: str) -> List[dict]:
        projection = {"_id": 1, "title": 1, "progress": 1}

        if progress_status == 'completada':
            progress_query = {"progress": 100}
        elif progress_status == 'en_progreso':
            progress_query = {"progress": {"$gt": 0, "$lt": 100}}
        elif progress_status == 'sin_iniciar':
            progress_query = {"progress": 0}
        else:
            raise ValueError("Estado de progreso no válido.")

        tasks_data = self.collection.find({"user_id": user_id, **progress_query}, projection)
        return [{"id": str(task["_id"]), "title": task["title"], "progress": task["progress"]} for task in tasks_data]
    
    def delete_task(self, task_id: str, user_id: str):
        try:
            object_id = ObjectId(task_id)
            result = self.collection.delete_one({"_id": object_id, "user_id": user_id})
            if result.deleted_count == 0:
                raise ValueError("No se encontró la tarea o el usuario no tiene permiso para eliminarla.")
        except Exception as e:
            print(f"Error al eliminar tarea: {e}")
            raise Exception("Error al eliminar tarea.")

    def get_weekly_progress(self, user_id: str, start_date: datetime, end_date: datetime):
        pipeline = [
            {"$match": {"user_id": user_id, "due_date": {"$gte": start_date, "$lt": end_date}}},
            {"$group": {
                "_id": None,
                "total_tasks": {"$sum": 1},
                "tasks_in_progress": {"$sum": {"$cond": [{"$and": [{"$gt": ["$progress", 0]}, {"$lt": ["$progress", 100]}]}, 1, 0]}},
                "tasks_completed": {"$sum": {"$cond": [{"$eq": ["$progress", 100]}, 1, 0]}},
                "tasks_unstarted": {"$sum": {"$cond": [{"$eq": ["$progress", 0]}, 1, 0]}},
            }}
        ]
        result = list(self.collection.aggregate(pipeline))
        if result:
            return result[0]
        else:
            return {
                "total_tasks": 0,
                "tasks_en_progreso": 0,
                "tasks_completada": 0,
                "tasks_sin_iniciar": 0
            }

    def get_progress_summary(self, user_id: str):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  
        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week - timedelta(seconds=1)
        
        last_week_progress = self.get_weekly_progress(user_id, start_of_last_week, end_of_last_week)
        current_week_progress = self.get_weekly_progress(user_id, start_of_week, today)
        
        return {
            "last_week": last_week_progress,
            "current_week": current_week_progress
        }
    
    def get_user_category_summary(self, user_id: str):
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$category",
                "total_tasks": {"$sum": 1},
                "tasks_in_progress": {"$sum": {"$cond": [{"$and": [{"$gte": ["$progress", 1]}, {"$lt": ["$progress", 100]}]}, 1, 0]}},
                "tasks_completed": {"$sum": {"$cond": [{"$eq": ["$progress", 100]}, 1, 0]}},
                "tasks_unstarted": {"$sum": {"$cond": [{"$eq": ["$progress", 0]}, 1, 0]}},
            }},
            {"$group": {
                "_id": None,
                "categories": {"$push": {
                    "category": "$_id",
                    "total_tasks": "$total_tasks",
                }},
                "total_tasks": {"$sum": "$total_tasks"},
                "total_in_progress": {"$sum": "$tasks_in_progress"},
                "total_completed": {"$sum": "$tasks_completed"},
                "total_unstarted": {"$sum": "$tasks_unstarted"},
            }},
            {"$project": {
                "_id": 0,
                "categories": 1,
                "total_tasks": 1,
                "total_en_progreso": 1,
                "total_completada": 1,
                "total_sin_iniciar": 1,
            }}
        ]
        result = list(self.db.tasks.aggregate(pipeline))
        if result:
            return result[0]
        else:
            return {
                "categories": [],
                "total_tasks": 0,
                "total_en_progreso": 0,
                "total_completada": 0,
                "total_sin_iniciar": 0
            }
        
    def get_tasks_for_notification(self, start_of_day, end_of_day):
        return list(self.collection.find({
            "progress": {"$lt": 100},
            "start_reminder_date": {"$gte": start_of_day, "$lte": end_of_day}
        }))
