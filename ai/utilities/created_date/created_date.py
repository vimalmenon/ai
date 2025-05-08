from datetime import datetime


def created_date() -> str:
    """Get the current date and time in ISO format."""
    return str(datetime.now().isoformat())
