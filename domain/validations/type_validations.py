def validate_type(task_type):
    valid_types = ['individual', 'grupal', 'asignar']
    if task_type not in valid_types:
        raise ValueError("Tipo de tarea no válido.")
