from __future__ import annotations
from irys_sdk.fund import Fund
from irys_sdk.tokens.base import BaseToken
from irys_sdk.tokens.ethereum import EthereumToken
from irys_sdk.upload import Upload
from irys_sdk.bundle.tags import Tags
from irys_sdk.utils import get_balance, get_price


class Uploader:
    token_config: "BaseToken"
    url: str
    uploader: "Upload"
    token: str
    funder: "Fund"

    def __init__(self, url, token, **opts):
        self.url = url
        self.token = token
        self.uploader = Upload(self)
        self.funder = Fund(self)
        token_ref = get_token(token)
        token_opts = opts.get("token_opts")
        self.token_config = token_ref(self, **token_opts)
        self.token_config.ready()

    @property
    def address(self) -> str:
        return self.token_config.address

    def upload(self, data: bytearray, tags: Tags = None, target: str = None, anchor: str = None):
        return self.uploader.upload(data, tags, target, anchor)

    def get_balance(self) -> int:
        return get_balance(self.url, self.token, self.address)

    def get_price(self, bytes: int) -> int:
        return get_price(self.url, self.token, bytes)

    def fund(self, amount_atomic: int, multiplier=1.0):
        return self.funder.fund(amount_atomic, multiplier)


def get_token(token: str) -> "BaseToken":
    match token:
        case "ethereum":
            return EthereumToken
        case _:
            raise Exception("Unknown/unsupported token {}".format(token))
