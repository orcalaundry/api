from abc import abstractmethod
from typing import Protocol, Tuple


class IESP32Service(Protocol):
    """
    "Interface" for CRUD methods associated to raspis.
    """

    @abstractmethod
    def create_machine(self, id: str, floor: int, pos: int):
        pass

    @abstractmethod
    def get_machine(self, id: str) -> Tuple[int, int] | None:
        pass
