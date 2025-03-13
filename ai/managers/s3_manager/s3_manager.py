from ai.config import env
from ai.managers.aws.session import Session
from ai.model import S3Item


class S3Manager:

    def __init__(self):
        session = Session().get_session()
        self.s3_resource = session.resource("s3")
        self.s3_client = session.client("s3")
        self.bucket = self.s3_resource.Bucket(name=env.bucket)

    def list_buckets(self):
        return self.s3_resource.list_buckets()

    def get_items(self):
        items = []
        for item in self.bucket.objects.all():
            items.append(
                S3Item(
                    name=item.key, last_modified=str(item.last_modified), size=item.size
                )
            )
        # objects = self.s3_client.list_objects_v2(
        #     Bucket=env.bucket,
        #     Delimiter='string',
        # )
        return items

    def put_item(self):
        pass

    def delete_item(self):
        pass

    def read_item(self):
        return ""

    def get_object(self, file_name: str):
        return self.s3_client.get_object(Bucket=env.bucket, Key=file_name)

    def upload_item(self, buffer, file_name: str):
        self.s3_client.upload_fileobj(buffer, env.bucket, file_name)
