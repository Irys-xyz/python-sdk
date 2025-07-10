from __future__ import annotations
from typing import Literal
from irys_sdk.fund import Fund
from irys_sdk.tokens.base import BaseToken
from irys_sdk.tokens.ethereum import EthereumToken
from irys_sdk.upload import Upload
from irys_sdk.bundle.tags import Tags
from irys_sdk.utils import get_balance, get_price

SupportedTokens = Literal["ethereum", "bnb"]


class Uploader:
    token: "BaseToken"
    url: str
    uploader: "Upload"

    funder: "Fund"

    def __init__(self, url, token: SupportedTokens, **opts):
        self.url = url
        self.uploader = Upload(self)
        self.funder = Fund(self)
        token_opts = opts.get("token_opts")
        self.token = get_token(
            token, self, **token_opts)  # type: ignore
        self.token.ready()

    @property
    def address(self) -> str:
        return self.token.address

    @property
    def token_name(self) -> str:
        return self.token.name

    def upload(self, data: bytearray, tags: Tags = None, target: str = None, anchor: str = None):
        return self.uploader.upload(data, tags, target, anchor)

    def get_balance(self) -> int:
        return get_balance(self.url, self.token_name, self.address)

    def get_price(self, bytes: int) -> int:
        return get_price(self.url, self.token_name, bytes)

    def fund(self, amount_atomic: int, multiplier=1.0):
        return self.funder.fund(amount_atomic, multiplier)


def get_token(token: SupportedTokens, irys: "Uploader", **token_opts) -> "BaseToken":
    match token:
        case "ethereum":

            return EthereumToken(irys, **token_opts)
        case "bnb":
            token_opts['provider_url'] = token_opts.get(
                "provider_url") or "https://bsc-dataseed.binance.org/"
            token_opts['name'] = "bnb"
            token_opts['ticker'] = "BNB"
            return EthereumToken(irys, **token_opts)
        case _:
            raise Exception("Unknown/unsupported token {}".format(token))
