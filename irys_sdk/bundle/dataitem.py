from __future__ import annotations
from typing import Any
from irys_sdk.bundle.constants import MAX_TAG_BYTES, MIN_BINARY_SIZE, SIG_CONFIG
from irys_sdk.bundle.sign import get_signature_data, sign
from irys_sdk.bundle.signers.index import index_to_type
from irys_sdk.bundle.tags import decode_tags, Tags
from irys_sdk.bundle.utils import byte_array_to_long, set_bytes
import hashlib
import base64
from base58 import b58encode


class DataItem:
    binary: bytearray
    _id: bytes

    def __init__(self, buffer: bytearray):
        self.binary = buffer
        self._id = []

    @staticmethod
    def is_data_item(item: Any) -> bool:
        isinstance(item, DataItem)

    @property
    def is_signed(self) -> bool:
        return len(self._id or []) > 0

    @property
    def signature_type(self) -> int:
        sig_type_int = byte_array_to_long(self.binary[0:2])
        sig_config = SIG_CONFIG.get(sig_type_int)
        if (sig_config == None):
            raise Exception(
                "invalid signature type {}".format(sig_type_int))
        return sig_type_int

    def is_valid(self) -> bool:
        return DataItem.verify(self.get_raw())

    @staticmethod
    def verify(bytes: bytearray) -> bool:
        if len(bytes) < MIN_BINARY_SIZE:
            return False
        item = DataItem(bytes)
        sig_type = item.signature_type
        tags_start = item.get_tags_start()
        number_of_tags = byte_array_to_long(bytes[tags_start: tags_start + 8])
        number_of_tags_byte_array = bytes[tags_start + 8: tags_start + 16]
        number_of_tag_bytes = byte_array_to_long(number_of_tags_byte_array)
        if number_of_tag_bytes > MAX_TAG_BYTES:
            return False
        if number_of_tags > 0:
            try:
                tags = decode_tags(
                    bytes[tags_start + 16: tags_start+16 + number_of_tag_bytes])
                if len(tags) != number_of_tags:
                    return False
            except:
                return False
        signer = index_to_type(sig_type)
        signature_data = get_signature_data(item)
        return signer.verify(item.raw_owner, signature_data, item.raw_signature)

    @property
    def id(self) -> str:
        return b58encode(self.raw_id).decode('utf-8')

    # set id

    @property
    def raw_id(self) -> bytes:
        return hashlib.sha256(self.raw_signature).digest()

    # set rawid

    @property
    def raw_signature(self):
        return self.binary[2:2+self.signature_length]

    @property
    def signature(self) -> bytearray:
        return base64.urlsafe_b64encode(self.raw_signature)

    # set raw owner

    @property
    def raw_owner(self) -> bytearray:
        return self.binary[2+self.signature_length:2+self.signature_length + self.owner_length]

    @property
    def signature_length(self) -> int:
        return SIG_CONFIG[self.signature_type]['sigLength']

    @property
    def owner(self) -> bytes:
        return base64.urlsafe_b64encode(self.raw_owner)

    @property
    def owner_length(self) -> int:
        return SIG_CONFIG[self.signature_type]['pubLength']

    @property
    def raw_target(self) -> bytearray:
        target_start = self.get_target_start()
        target_present = self.binary[target_start] == 1
        return self.binary[target_start + 1: target_start + 33] if target_present else bytearray()

    # TODO target

    @property
    def raw_anchor(self) -> bytearray:
        anchor_start = self.get_anchor_start()
        anchor_present = self.binary[anchor_start] == 1
        return self.binary[anchor_start + 1: anchor_start + 33] if anchor_present else bytearray()

    # TODO anchor

    @property
    def raw_tags(self) -> bytearray:
        tags_start = self.get_tags_start()
        tags_size = self.get_tags_size()
        return self.binary[tags_start+16:tags_start+16+tags_size]

    @property
    def tags(self) -> Tags:
        tags_count = self.get_tags_count()
        if tags_count == 0:
            return []
        return decode_tags(self.raw_tags)

    def get_start_of_data(self) -> int:
        tags_start = self.get_tags_start()
        tags_size = self.get_tags_size()
        return tags_start + 16 + tags_size

    @property
    def raw_data(self) -> bytearray:
        data_start = self.get_start_of_data()
        return self.binary[data_start:]

    def get_tags_count(self) -> int:
        tags_start = self.get_tags_start()
        return byte_array_to_long(self.binary[tags_start:tags_start+8])

    def get_tags_size(self) -> int:
        tags_start = self.get_tags_start()
        return byte_array_to_long(self.binary[tags_start+8:tags_start+16])

    def get_raw(self) -> bytearray:
        return self.binary

    def sign(self, signer: "Signer") -> bytearray:
        self._id = sign(self, signer)
        return self.raw_id

    def set_signature(self, signature: bytearray):
        set_bytes(self.binary, signature, 2)
        self._id = hashlib.sha256(signature).digest()

    def get_tags_start(self) -> int:
        target_start = self.get_target_start()
        target_present = self.binary[target_start] == 1
        tags_start = target_start + (33 if target_present else 1)
        anchor_present = self.binary[tags_start] == 1
        tags_start += (33 if anchor_present else 1)
        return tags_start

    def get_target_start(self) -> int:
        return 2 + self.signature_length + self.owner_length

    def get_anchor_start(self) -> int:
        anchor_start = self.get_target_start() + 1
        target_present = self.binary[self.get_target_start()] == 1
        anchor_start += 32 if target_present else 0
        return anchor_start
