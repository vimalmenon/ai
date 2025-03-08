from ai.config.env import env
from ai.managers.aws.session import Session


class DbManager:
    def __init__(self):
        session = Session().get_session()
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table(env.table)

    def create(self):
        return self.table.creation_date_time

    def add_item(self, item):
        return self.table.put_item(Item=item)

    def remove_item(self, item):
        return self.table.delete_item(Key=item)

    def query_items(self):
        pass

    def update_item(self):
        pass
