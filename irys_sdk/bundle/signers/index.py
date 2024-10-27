from __future__ import annotations
import importlib


def index_to_type(index: int):
    match index:
        case 3:
            # lazy import to prevent dep cycle
            mod = importlib.import_module("irys_sdk.bundle.signers.ethereum")
            return mod.EthereumSigner
            # from irys_sdk.bundle.signers.ethereum import EthereumSigner
            # return EthereumSigner
