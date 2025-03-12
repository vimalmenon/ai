from ai.managers.aws.session import Session


class S3Manager:

    def __init__(self):
        self.session = Session().get_session()

    def get_items(self):
        pass

    def put_item(self):
        pass

    def delete_item(self):
        pass

    def read_item(self):
        pass
