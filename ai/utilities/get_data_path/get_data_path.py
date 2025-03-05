import os


def get_data_path(file: str) -> str:
    return f"{os.getcwd()}/ai/data/{file}"
