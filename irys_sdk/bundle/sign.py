from __future__ import annotations
import hashlib
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from irys_sdk.bundle.dataitem import DataItem
    from irys_sdk.bundle.signers.signer import Signer


def sign(item: 'DataItem', signer: Signer) -> bytearray:
    (signature, id) = get_signature_and_id(item, signer)
    item.set_signature(signature)
    return id


def get_signature_and_id(item: 'DataItem', signer: Signer) -> (bytearray, bytearray):
    signature_data = get_signature_data(item)
    signature_bytes = signer.sign(signature_data)
    id_bytes = hashlib.sha256(signature_bytes).digest()
    return (signature_bytes,  id_bytes)


def get_signature_data(item: 'DataItem') -> bytearray:
    arr = [
        b"dataitem",
        b"1",
        str(item.signature_type).encode(),
        item.raw_owner,
        item.raw_target,
        item.raw_anchor,
        item.raw_tags,
        item.raw_data
    ]
    dh = deep_hash(arr)
    return dh


def deep_hash(data: list[bytearray]) -> bytearray:
    if type(data) == list:
        tag = b"list" + str(len(data)).encode()
        return deep_hash_chunks(data, hashlib.sha384(tag).digest())
    else:
        tag = b"blob" + str(len(data)).encode()
    tagged_hash = hashlib.sha384(tag).digest() + hashlib.sha384(data).digest()
    return hashlib.sha384(tagged_hash).digest()


def deep_hash_chunks(chunks, acc: bytearray):
    if len(chunks) < 1:
        return acc
    hash_pair = acc + deep_hash(chunks[0])
    new_acc = hashlib.sha384(hash_pair).digest()
    return deep_hash_chunks(chunks[1:], new_acc)
