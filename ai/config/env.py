import os

from pydantic import BaseModel


class Env(BaseModel):
    temperature: float = float(os.getenv("TEMPERATURE", 0.0))
    notes_path: str = f"{os.getcwd()}/ai/data/notes/data.txt"
    debug: bool = bool(os.getenv("DEBUG", False))
    table: str = str(os.getenv("TABLE"))
    aws_client_id: str = str(os.getenv("AWS_CLIENT_ID"))
    aws_secret: str = str(os.getenv("AWS_SECRET"))
    supported_llm: list[str] = os.getenv("SUPPORTED_LLM", "").split(",")
    port: int = int(os.getenv("PORT", 8000))
    bucket: str = str(os.getenv("S3_BUCKET"))
    eden_ai_api: str = str(os.getenv("EDEN_AI_API"))
    openai_api: str = str(os.getenv("OPENAI_API_KEY"))
    aws_sqs: str = str(os.getenv("AWS_SQS"))
    aws_region: str = str(os.getenv("AWS_REGION"))

    def __init__(self, **data):
        super().__init__(**data)
        self.temperature = float(os.getenv("TEMPERATURE", 0.0))
        self.notes_path = f"{os.getcwd()}/ai/data/notes/data.txt"
        self.debug = bool(os.getenv("DEBUG", False))
        self.table = str(os.getenv("TABLE"))
        self.aws_client_id = str(os.getenv("AWS_CLIENT_ID"))
        self.aws_secret = str(os.getenv("AWS_SECRET"))
        self.supported_llm = os.getenv("SUPPORTED_LLM", "").split(",")
        self.port = int(os.getenv("PORT", 8000))
        self.bucket = str(os.getenv("S3_BUCKET"))
        self.eden_ai_api = str(os.getenv("EDEN_AI_API"))
        self.openai_api = str(os.getenv("OPENAI_API_KEY"))
        self.aws_sqs = str(os.getenv("AWS_SQS"))
        self.aws_region = str(os.getenv("AWS_REGION"))


env = Env()
