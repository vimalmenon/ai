import boto3

from ai.config.env import env
from ai.managers.aws.session import Session

dynamodb = boto3.resource("dynamodb")


class DbManager:
    def __init__(self):
        session = Session().get_session()
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table(env.table)

    def create(self):
        return self.table.creation_date_time

    def add_item(self):
        pass

    def remove_item(self):
        pass

    def query_items(self):
        pass
