from abc import ABC, abstractmethod
from sentinelzero.core.models import ProtocolSnapshot

class DataSource(ABC):

    @abstractmethod
    def fetch(self, protocol_name: str) -> ProtocolSnapshot:
        pass

