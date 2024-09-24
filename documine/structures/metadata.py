
class Metadata:
    def __init__(self, **kwargs):
        self.page_number = kwargs.get('page_number')
        self.file_name = kwargs.get('file_name')
        self.content_type = kwargs.get('content_type')
        self.tag_name = kwargs.get('tag_name')
        self.attributes = kwargs.get('attributes', {})
        self.order = kwargs.get('order')
        self.xpath = kwargs.get('xpath')
        self.links = kwargs.get('links', [])
        # TODO: Add more if necessary