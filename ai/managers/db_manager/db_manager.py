from botocore.exceptions import ClientError

from ai.config.env import env
from ai.managers.aws.session import Session


class DbManager:
    def __init__(self):
        session = Session().get_session()
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table(env.table)

    def add_item(self, item):
        return self.table.put_item(Item=item)

    def remove_item(self, data):
        return self.table.delete_item(Key=data)

    def query_items(self, keys):
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
