from documine.structures.metadata import Metadata


class Element:
    def __init__(self, content: str, metadata: Metadata):
        self.content = content
        self.metadata = metadata


class Title(Element):
    pass


class Text(Element):
    pass


class List(Element):
    def __init__(self, items: list, metadata: Metadata):
        super().__init__(content=items, metadata=metadata)


class Table(Element):
    def __init__(self, data: list, metadata: Metadata):
        super().__init__(content=data, metadata=metadata)


class Link(Element):
    def __init__(self, text: str, href: str, metadata: Metadata):
        super().__init__(content=text, metadata=metadata)
        self.href = href
