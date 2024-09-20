import logging
from typing import List
from documine.parser.base import BaseParser
from documine.structures import Element

logger = logging.getLogger(__name__)

class HTMLParser(BaseParser):
    def parse(self, file_path: str) -> List[Element]:
        pass