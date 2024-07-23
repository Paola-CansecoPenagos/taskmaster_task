def validate_text_length(text, min_len, max_len, field_name):
    if not min_len <= len(text) <= max_len:
        raise ValueError(f"{field_name} debe tener entre {min_len} y {max_len} caracteres.")