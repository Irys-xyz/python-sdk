import codecs
from typing import Any
from irys_sdk.bundle.signers.signer import Signer
from irys_sdk.bundle.constants import SIG_CONFIG
from eth_account import Account
from eth_account.messages import encode_defunct, _hash_eip191_message
from eth_account._utils.signing import to_standard_v
from eth_keys import keys


class EthereumSigner(Signer):
    account: Account
    public_key = None
    private_key = None
    signature_type = 3
    signature_length = SIG_CONFIG[3]['sigLength']
    owner_length = SIG_CONFIG[3]['pubLength']

    def __init__(self, private_key: str):
        private_key = private_key[2:] if private_key.startswith(
            "0x") else private_key
        dec = codecs.decode(private_key, "hex")
        self.private_key = keys.PrivateKey(dec)
        self.public_key = b'\x04' + \
            self.private_key.public_key.to_bytes()

    def sign(self, message: bytearray, **opts: Any) -> bytearray:
        msg = encode_defunct(primitive=message)

        acc = Account.from_key(self.private_key)
        signature = (acc.sign_message(msg)).signature.hex()
        return bytearray.fromhex(signature[2:] if signature.startswith("0x") else signature)

    @staticmethod
    def verify(pubkey: bytearray, message: bytearray, signature: bytearray, **opts: Any) -> bool:
        msg = encode_defunct(primitive=message)
        msg_hash = _hash_eip191_message(msg)
        # trim pubkey
        pubkey = keys.PublicKey(
            pubkey if len(pubkey) == 64 else pubkey[1:])
        # standardize v value
        signature[64] = to_standard_v(signature[64])
        signature = keys.Signature(signature)
        valid = keys.ecdsa_verify(msg_hash, signature, pubkey)
        return valid
