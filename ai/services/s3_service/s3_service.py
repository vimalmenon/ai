from ai.managers import S3Manager


class S3Service:

    def get_items(self):
        return S3Manager().get_items()
