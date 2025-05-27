import io
from collections.abc import MutableSequence
from typing import Dict
import avro.schema
from avro.io import DatumReader, DatumWriter

# name value
Tag = tuple[str, str]
# Tags aren't defined as a dict, as the spec allows for duplicate tag names/keys
Tags = list[Tag]

schema = avro.schema.parse("""
{"type": "array",
    "items": {
        "type": "record",
        "name": "Tag",
        "fields": [
            { "name": "name", "type": "string" },
            { "name": "value", "type": "string" }
        ]
    }
}
""")


def from_dict(tags: Dict[str, str]) -> Tags:
    return list(tags.items())


def encode_tags(tags: MutableSequence[Tag]) -> bytes:
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write(
        list(map(lambda x: {"name": x[0], "value": x[1]}, tags)), encoder)

    raw_bytes = bytes_writer.getvalue()

    return raw_bytes


def decode_tags(tag_bytes: bytes) -> MutableSequence[Tag]:
    reader = DatumReader(schema)
    bytes_reader = io.BytesIO(tag_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    res = reader.read(decoder)

    return list(map(lambda x: [x["name"], x["value"]], res))
