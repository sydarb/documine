from documine.structures.metadata import Metadata


class Element:
    def __init__(self, content: str, metadata: Metadata):
        self.content = content
        self.metadata = metadata


class TitleElement(Element):
    pass


class TextElement(Element):
    pass


class ListElement(Element):
    def __init__(self, items: list, metadata: Metadata):
        super().__init__(content=items, metadata=metadata)


class TableElement(Element):
    def __init__(self, data: list, metadata: Metadata):
        super().__init__(content=data, metadata=metadata)


class LinkElement(Element):
    def __init__(self, text: str, href: str, metadata: Metadata):
        super().__init__(content=text, metadata=metadata)
        self.href = href
