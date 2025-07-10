from __future__ import annotations
from abc import abstractmethod
from typing import Any, Tuple
from irys_sdk.types import Tx

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from irys_sdk.bundle.signers.signer import Signer


class BaseToken:
    address: str
    name: str
    ticker: str
    base: tuple[str, int]

    def __init__(self):
        pass

    @abstractmethod
    def get_tx(self, tx_id: str) -> Tx:
        pass

    @abstractmethod
    def owner_to_address(self, pub: bytearray) -> str:
        pass

    @abstractmethod
    def sign(self, data: bytearray) -> bytearray:
        pass

    @abstractmethod
    def get_signer(self) -> "Signer":
        pass

    @abstractmethod
    def get_fee(self, amount, to=None) -> int:
        pass

    @abstractmethod
    def create_tx(self, amount: int, to: str, fee=None) -> Tuple[str | None, Any]:
        pass

    @abstractmethod
    def send_tx(self, tx: Any) -> Any:
        pass

    @abstractmethod
    def get_public_key(self) -> bytearray:
        pass

    @abstractmethod
    def ready(self):
        pass
