import re

def validate_text(text,field_name):
    patterns = [
        r"<script.*?>.*?</script>",
        r"<iframe.*?>.*?</iframe>",
        r"<(object|embed|applet|link|style|img|meta|base).*?>",
        r"on[a-z]+=\"[^\"]*\"",
        r"href=\"javascript:[^\"]*\"",
        r"src=\"javascript:[^\"]*\"",
        r"style=\".*?expression\([^)]*\).*?\""
    ]
    if any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns):
        raise ValueError(f"{field_name} contiene contenido no permitido.")
