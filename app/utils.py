import re 

def is_valid_email(text: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", text))

def is_valid_phone(text: str) -> bool:
    return bool(re.match(r"^\+?[0-9\s\-]{7,15}$", text))