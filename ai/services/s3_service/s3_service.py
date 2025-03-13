from ai.managers import S3Manager


class S3Service:

    def get_items(self):
        return S3Manager().get_items()

    def read_item(self, _):
        return S3Manager().read_item()

    def upload_item(self):
        return ""
