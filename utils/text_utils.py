from markupsafe import escape
import json

def escape_html(text):
    return escape(text)

def escape_javascript(text):
    return json.dumps(text)

def trim_text(text):
    return text.strip()