from abc import ABC, abstractmethod
from typing import Any


class Reader(ABC):
    @abstractmethod
    def read(self) -> Any:
        ...

