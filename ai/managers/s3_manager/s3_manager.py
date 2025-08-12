from ai.config import Env
from ai.managers.aws.session import Session
from ai.model import S3Item
from ai.model.enums import DbTable


class S3Manager:
    table = DbTable.AI_S3.value

    def __init__(self):
        session = Session().get_session()
        self.s3_resource = session.resource("s3")
        self.s3_client = session.client("s3")
        self.env = Env()
        self.bucket = self.s3_resource.Bucket(name=self.env.bucket)

    def list_buckets(self):
        return self.s3_resource.list_buckets()

    def get_items(self) -> list[S3Item]:
        return [
            S3Item(name=item.key, last_modified=str(item.last_modified), size=item.size)
            for item in self.bucket.objects.all()
        ]

    def delete_item(self, file_name: str):
        return self.s3_client.delete_object(Bucket=self.env.bucket, Key=file_name)

    def get_object(self, file_name: str):
        return self.s3_client.get_object(Bucket=self.env.bucket, Key=file_name)

    def upload_item(self, buffer, file_name: str):
        self.s3_client.upload_fileobj(buffer, self.env.bucket, file_name)
