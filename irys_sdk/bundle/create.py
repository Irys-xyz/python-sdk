import base64
from irys_sdk.bundle.dataitem import DataItem
from irys_sdk.bundle.tags import encode_tags, Tags
from irys_sdk.bundle.signers.signer import Signer
from irys_sdk.bundle.utils import long_to_8_byte_array, set_bytes, short_to_2_byte_array


def create_data(data: bytearray | str, signer: Signer, tags: Tags = None, target: str = None, anchor: str = None) -> DataItem:
    owner = signer.public_key
    # target = opts.get('target')
    target = None if target == None else base64.urlsafe_b64decode(target)
    target_length = 1 + (len(target) if target != None else 0)
    # anchor = opts.get('anchor')
    anchor = None if anchor == None else anchor.encode()
    anchor_length = 1 + (len(anchor) if anchor != None else 0)

    opt_tags = tags
    tags = None if opt_tags == None else encode_tags(opt_tags)
    tags_length = 16 + (0 if tags == None else len(tags))

    data = data.encode() if isinstance(data, str) else data

    data_length = len(data)

    length = 2 + signer.signature_length + signer.owner_length + \
        target_length + anchor_length + tags_length + data_length

    bytes = bytearray(length)

    set_bytes(bytes, short_to_2_byte_array(signer.signature_type), 0)

    set_bytes(bytes, bytearray(signer.signature_length), 2)

    if len(owner) != signer.owner_length:
        raise Exception("Owner must be {} bytes, but was incorrectly {} bytes".format(
            signer.owner_length, len(owner)))

    set_bytes(bytes, owner, 2 + signer.signature_length)

    position = 2 + signer.signature_length + signer.owner_length

    bytes[position] = 0 if target == None else 1
    if (target != None):
        if len(target) != 32:
            raise Exception(
                "Target must be 32 bytes, was incorrectly {} bytes".format(len(target)))
        set_bytes(bytes, target, position + 1)

    anchor_start = position + target_length
    tags_start = anchor_start + 1
    bytes[anchor_start] = 0 if anchor == None else 1
    if (anchor != None):
        tags_start += len(anchor)
        if (len(anchor) != 32):
            raise Exception(
                "Anchor must be 32 bytes, was incorrectly {} bytes".format(len(anchor)))
        set_bytes(bytes, anchor, anchor_start + 1)

    set_bytes(bytes, long_to_8_byte_array(
        0 if opt_tags == None else len(opt_tags)), tags_start)

    bytes_count = long_to_8_byte_array(0 if tags == None else len(tags))
    set_bytes(bytes, bytes_count, tags_start + 8)

    if (tags != None):
        set_bytes(bytes, tags, tags_start + 16)

    data_start = tags_start + tags_length

    set_bytes(bytes, data, data_start)

    return DataItem(bytes)
