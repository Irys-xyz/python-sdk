type Tx = {
    "from": str,
    "to": str,
    "amount": int,
    "blockHeight": int | None,
    "pending": bool,
    "confirmed": bool
}
