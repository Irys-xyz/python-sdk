from collections.abc import MutableSequence

from transaction import Transaction, Tag
import requests


def upload(url: str, bytes: str | bytearray, tags: MutableSequence[Tag] | None = None) -> None:
    response = requests.post(url, data=bytes)
    if response.ok:
        return
    else:
        raise Exception(f"Failed to upload tx - {response.text}")


def upload_transaction(url: str, tx: Transaction):
    response = requests.post(url, data=tx.binary)
    if response.ok:
        return
    else:
        raise Exception(f"Failed to upload tx - {response.text}")
