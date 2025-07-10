from __future__ import annotations
from typing import Literal
from irys_sdk.client import SupportedTokens, Uploader


class Builder:
    _node_url = "https://uploader.irys.xyz"
    _network = "mainnet"
    token_opts = {"provider_url": None}

    def __init__(self, token: SupportedTokens):
        self.token = token

    @property
    def network(self):
        self._network

    def network(self, network: Literal["mainnet", "devnet"]):
        match network:
            case "mainnet":
                self._node_url = "https://uploader.irys.xyz"
            case "devnet":
                self._node_url = "https://devnet.irys.xyz"
            case _:
                raise Exception(
                    "invalid network, expected 'mainnet' or 'devnet'")

        self._network = network
        return self

    # @property
    # def rpc_url(self):
    #     self.token_opts["provider_url"]

    def rpc_url(self, rpc_url: str):
        self.token_opts["provider_url"] = rpc_url
        return self

    # @property
    # def wallet(self):
    #     return self.token_opts["wallet"]

    def wallet(self, wallet: str):
        self.token_opts["wallet"] = wallet
        return self

    def node_url(self, node_url: str):
        self._node_url = node_url
        return self

    # @property
    # def url(self) -> str:
    #     return self._node_url

    def build(self) -> "Uploader":
        if (self.network == "devnet" and self.rpc_url == None):
            raise Exception("rpc url must be provided when using devnet")

        uploader = Uploader(self._node_url, self.token,
                            token_opts=self.token_opts)
        return uploader
