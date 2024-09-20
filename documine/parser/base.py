from abc import ABC, abstractmethod
from typing import List
from documine.structures.elements import Element

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> List[Element]:
        pass
