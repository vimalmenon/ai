from datetime import datetime


class DateHelper:
    @staticmethod
    def created_date() -> str:
        """Get the current date and time in ISO format."""
        return str(datetime.now().isoformat())


def created_date() -> str:
    """Get the current date and time in ISO format."""
    return str(datetime.now().isoformat())
