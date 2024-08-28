from apscheduler.schedulers.background import BackgroundScheduler
import pymongo
from datetime import datetime

client = pymongo.MongoClient()
db_task = client[]
tasks_collection = db_task[]
db_not = client[]
notifications_collection = db_not[]

def create_notifications():
    now = datetime.now()
    tasks = tasks_collection.find({
        "start_reminder_date": {"$lte": now},
        "due_date": {"$gte": now},
        "progress": {"$lt": 100}
    })

    for task in tasks:
        task_id = task['_id']
        user_id = task['user_id']
        title = task['title']
        start_reminder_time = datetime.strptime(task['start_reminder_time'], '%H:%M:%S').time()
        end_reminder_time = datetime.strptime(task['end_reminder_time'], '%H:%M:%S').time()
        due_time = datetime.strptime(task['due_time'], '%H:%M:%S').time()

        reminder_start_datetime = datetime.combine(now.date(), start_reminder_time)
        reminder_end_datetime = datetime.combine(now.date(), end_reminder_time)
        due_datetime = datetime.combine(now.date(), due_time)

        # Generar mensajes basados en el progreso
        if task['progress'] == 0:
            messages = [
                f"No olvides de {title}",
                f"Recuerda de {title}"
            ]
        else:
            messages = [
                f"Ya casi terminas {title}",
                f"Falta poco para completar {title}"
            ]

        # Crear notificaciones dentro del rango de tiempo de recordatorio
        current_time = now.time()
        if start_reminder_time <= current_time <= end_reminder_time:
            message = messages[0]
            notification = {
                "task_id": str(task_id),
                "user_id": user_id,
                "message": message,
            }
            notifications_collection.insert_one(notification)
        
        if now.date() == task['due_date'].date() and current_time >= due_time:
            message = f"Último recordatorio para {title}"
            notification = {
                "task_id": str(task_id),
                "user_id": user_id,
                "message": message,
            }
            notifications_collection.insert_one(notification)

scheduler = BackgroundScheduler()
scheduler.add_job(create_notifications, 'interval', minutes=30, id='task_reminders')
