from botocore.exceptions import ClientError

from ai.config import Env
from ai.managers.aws.session import Session


class DbManager:
    def __init__(self):
        env = Env()
        session = Session().get_session()
        dynamodb = session.resource("dynamodb", region_name=env.aws_region)
        self.table = dynamodb.Table(env.table)

    def add_item(self, item: dict):
        return self.table.put_item(Item=item)

    def remove_item(self, data: dict):
        return self.table.delete_item(Key=data)

    def query_items(self, keys) -> list:
        try:
            return self.table.query(
                Select="ALL_ATTRIBUTES",
                ConsistentRead=True,
                KeyConditionExpression=(keys),
            )["Items"]
        except ClientError:
            return []

    def update_item(self, **data):
        return self.table.update_item(**data)

    def get_item(self, key):
        try:
            value = self.table.get_item(Key=key)
            if "Item" in value:
                return value["Item"]
            return None
        except ClientError:
            return None

    def get_batch_data(self):
        pass
