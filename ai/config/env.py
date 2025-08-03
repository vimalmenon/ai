import json
import os
from dataclasses import dataclass


@dataclass
class Env:
    temperature: float
    notes_path: str
    table: str
    aws_client_id: str
    aws_secret: str
    supported_llm: list[str]
    port: int
    bucket: str
    eden_ai_api: str
    openai_api: str
    aws_sqs: str
    aws_secret_manager: str
    aws_region: str
    debug: bool = False

    def __init__(self, **data):
        secrets = self.get_from_aws_secret()
        self.temperature = float(
            self.__get_from_env_or_secret(secrets, "TEMPERATURE", 0.0)
        )
        self.notes_path = f"{os.getcwd()}/ai/data/notes/data.txt"
        self.debug = bool(self.__get_from_env_or_secret(secrets, "DEBUG", False))
        self.table = str(self.__get_from_env_or_secret(secrets, "AWS_TABLE", ""))
        self.aws_client_id = str(
            self.__get_from_env_or_secret(secrets, "AWS_CLIENT_ID", "")
        )
        self.aws_secret = str(self.__get_from_env_or_secret(secrets, "AWS_SECRET", ""))
        self.supported_llm = self.__get_from_env_or_secret(
            secrets, "SUPPORTED_LLM", ""
        ).split(",")
        self.port = int(self.__get_from_env_or_secret(secrets, "PORT", 8000))
        self.bucket = str(self.__get_from_env_or_secret(secrets, "S3_BUCKET", ""))
        self.eden_ai_api = str(
            self.__get_from_env_or_secret(secrets, "EDEN_AI_API", "")
        )
        self.openai_api = str(
            self.__get_from_env_or_secret(secrets, "OPENAI_API_KEY", "")
        )
        self.aws_sqs = str(self.__get_from_env_or_secret(secrets, "AWS_SQS", ""))
        self.aws_secret_manager = str(
            self.__get_from_env_or_secret(secrets, "AWS_SECRET_MANAGER", "")
        )
        self.aws_region = str(self.__get_from_env_or_secret(secrets, "AWS_REGION", ""))

    def __get_from_env_or_secret(self, secrets: dict[str, str], key: str, default=None):
        """
        Fetches a value from environment variables or AWS Secrets Manager.
        :param key: The key to fetch.
        :return: The value of the key.
        """
        return os.getenv(key, secrets.get(key, default))

    def get_from_aws_secret(self) -> dict[str, str]:
        """
        Fetches a secret from AWS Secrets Manager.
        :param key: The key of the secret to fetch.
        :return: The value of the secret.
        """
        import boto3
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_CLIENT_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        client = session.client("secretsmanager")
        try:
            response = client.get_secret_value(SecretId=os.getenv("AWS_SECRET_MANAGER"))
            return json.loads(response["SecretString"])
        except ClientError:
            return {}
        except Exception as e:
            logging.exception("Unexpected error occurred while fetching AWS secret")
            return {}
