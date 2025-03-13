import io

from ai.managers import S3Manager


class S3Service:

    def get_items(self):
        return S3Manager().get_items()

    def read_item(self, file_name: str):
        item = S3Manager().get_object(file_name)
        return item["Body"].read()

    def upload_item(self, data):
        f = io.StringIO(data.data)
        S3Manager().upload_item(io.BytesIO(f.read().encode("utf8")), data.name)
        return ""

    def sync_bucket(self):
        return ""
