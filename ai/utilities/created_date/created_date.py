from datetime import datetime


def created_date():
    return str(datetime.now().isoformat())
