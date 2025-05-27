from typing import TypedDict, Optional

Tx = TypedDict('Tx', {
    'from': str,
    'to': str,
    'amount': int,
    'blockHeight': Optional[int],
    'pending': bool,
    'confirmed': bool
})
