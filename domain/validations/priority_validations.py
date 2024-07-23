def validate_priority(priority):
    valid_priorities = ['alta', 'media', 'baja']
    if priority not in valid_priorities:
        raise ValueError("Prioridad no válida.")
