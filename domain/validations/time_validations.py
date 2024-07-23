from datetime import datetime

def validate_time_order(start_reminder_time_str, end_reminder_time_str):
    start_reminder_time = datetime.strptime(start_reminder_time_str, '%H:%M:%S').time()
    end_reminder_time = datetime.strptime(end_reminder_time_str, '%H:%M:%S').time()
    if end_reminder_time <= start_reminder_time:
        raise ValueError('La hora de fin de los recordatorios no puede ser anterior o igual a la hora de inicio.')
