from __future__ import annotations
from typing import Any
from eth_account import Account
from web3 import Web3
from irys_sdk.bundle.signers.ethereum import EthereumSigner
from irys_sdk.tokens.base import BaseToken
from eth_hash.auto import keccak

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from irys_sdk.client import Uploader


class EthereumToken(BaseToken):
    irys: "Uploader" = None
    address: str = None
    _provider_instance = None
    name = "ethereum",
    ticker = "ETH"
    base = ("wei", int(1e18))

    def __init__(self, irys, **kwargs):
        self.irys = irys

        self.provider_url = kwargs.get(
            "provider_url") or "https://cloudflare-eth.com/"
        self.name = kwargs.get("name") or "ethereum"
        self.ticker = kwargs.get("ticker") or "ETH"

        self._wallet = kwargs.get("wallet")
        if self._wallet == None:
            raise Exception("missing required wallet arg")
        pass

    def get_provider(self):
        if self._provider_instance == None:
            self._provider_instance = Web3(
                Web3.HTTPProvider(self.provider_url))
        return self._provider_instance

    def get_public_key(self) -> bytearray:
        return self.get_signer().public_key

    def get_signer(self):
        return EthereumSigner(self._wallet)

    def get_tx(self, tx_id: str):
        provider = self.get_provider()
        return provider.eth.get_transaction(tx_id)

    def owner_to_address(self, pub: bytearray) -> str:
        pubkey = pub if len(pub) == 64 else pub[1:]
        kek = keccak(pubkey)
        return "0x" + kek[-20:].hex()

    def ready(self):
        self.address = self.owner_to_address(self.get_public_key())

    def create_tx(self, amount: int, to: str, fee=None):
        provider = self.get_provider()
        chain_id = provider.eth.chain_id
        nonce = provider.eth.get_transaction_count(
            Web3.to_checksum_address(self.address))
        txb = {
            'to': to,
            'value': amount,
            "gas": 100000,
            "maxFeePerGas": 2000000000,
            "maxPriorityFeePerGas": 2000000000,
            'nonce': nonce,
            'chainId': chain_id
        }

        signed_tx = Account.sign_transaction(txb, self._wallet)

        return (signed_tx)

    def send_tx(self, tx: Any) -> Any:
        provider = self.get_provider()
        # res = provider.eth.send_raw_transaction(tx.raw_transaction)
        # return res.to_0x_hex()

        res = provider.eth.send_raw_transaction(tx.rawTransaction)
        return res.hex()
