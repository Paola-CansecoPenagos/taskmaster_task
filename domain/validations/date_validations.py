from dateutil.parser import parse
from datetime import datetime

def validate_start_reminder_date(start_reminder_date_str):
    start_reminder_date = parse(start_reminder_date_str)
    if start_reminder_date.date() < datetime.now().date():
        raise ValueError('La fecha de inicio de recordatorios no puede ser en el pasado.')

def validate_due_date(due_date_str):
    due_date = parse(due_date_str)
    if due_date.date() < datetime.now().date():
        raise ValueError('La fecha límite no puede ser en el pasado.')

def validate_date_order(start_reminder_date_str, due_date_str):
    start_reminder_date = parse(start_reminder_date_str)
    due_date = parse(due_date_str)
    if start_reminder_date.date() > due_date.date():
        raise ValueError('La fecha de inicio de recordatorios no puede ser posterior a la fecha límite.')
