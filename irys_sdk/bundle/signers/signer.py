from abc import abstractmethod
from typing import Any


class Signer():

    @property
    @abstractmethod
    def public_key(self) -> bytearray:
        pass

    @property
    @abstractmethod
    def signature_type(self) -> int:
        pass

    @property
    @abstractmethod
    def signature_length(self) -> int:
        pass

    @property
    @abstractmethod
    def owner_length(self) -> int:
        pass

    @abstractmethod
    def sign(self, message: bytearray, **opts: Any) -> bytearray:
        pass

    @abstractmethod
    # @staticmethod
    def verify(pubkey: bytearray, message: bytearray, signature: bytearray, **opts: Any) -> bool:
        pass
