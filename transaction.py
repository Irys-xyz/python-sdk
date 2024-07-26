from collections.abc import MutableSequence
from tags import Tag

class Transaction:
    binary: bytearray

    def __init__(self, buffer: bytearray):
        self.binary = buffer

def create_transaction(data: str | bytearray, tags: MutableSequence[Tag]) -> Transaction:

    return Transaction(bytearray(data))
