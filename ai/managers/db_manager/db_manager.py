import uuid
from datetime import datetime

from ai.config.env import env
from ai.managers.aws.session import Session


class DbManager:
    def __init__(self):
        session = Session().get_session()
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table(env.table)

    def create(self):
        return self.table.creation_date_time

    def add_item(self, data):
        return self.table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "app": "vm#vim",
                "describe": data.describe,
                "command": data.command,
                "language": data.language,
                "tags": data.tags,
                "creation_date": datetime.now().isoformat(),
            }
        )

    def remove_item(self):
        pass

    def query_items(self):
        pass

    def update_item(self):
        pass
