import boto3

from ai.config import Env


class Session:
    def get_session(self):
        env = Env()
        return boto3.Session(
            aws_access_key_id=env.aws_client_id,
            aws_secret_access_key=env.aws_secret,
            region_name=env.aws_region,
        )
