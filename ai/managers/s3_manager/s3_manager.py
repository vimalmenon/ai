from ai.config import env
from ai.managers.aws.session import Session


class S3Manager:

    def __init__(self):
        session = Session().get_session()
        self.s3_resource = session.resource("s3")
        self.bucket = self.s3_resource.Bucket(name=env.bucket)

    def list_buckets(self):
        return self.s3_resource.list_buckets()

    def get_items(self):
        items = []
        for item in self.bucket.objects.all():
            items.append(item.key)
        return items

    def put_item(self):
        pass

    def delete_item(self):
        pass

    def read_item(self):
        pass
