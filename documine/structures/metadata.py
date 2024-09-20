
class Metadata:
    def __init__(self, **kwargs):
        self.page_number = kwargs.get('page_number')
        self.file_name = kwargs.get('file_name')
        self.content_type = kwargs.get('content_type')