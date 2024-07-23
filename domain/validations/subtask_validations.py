def validate_subtasks(subtasks):
    if not subtasks:
        raise ValueError("Debe haber al menos una subtarea.")
    if not all(3 <= len(subtask['title']) <= 150 for subtask in subtasks):
        raise ValueError("Cada subtarea debe tener entre 3 y 150 caracteres.")
