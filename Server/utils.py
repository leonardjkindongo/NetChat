from datetime import datetime

def format_message(username: str, msg: str) -> str:
    """
    Add a timestamp and username to the message.
    Example:
    [12:45:10] Alice: Hello everyone!
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    return f"[{timestamp}] {username}: {msg}"

def log_event(event: str):
    """
    Print server events such as connections or disconnections.
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [SERVER] {event}")
