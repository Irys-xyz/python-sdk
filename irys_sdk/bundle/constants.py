

MAX_TAG_BYTES = 4096
MIN_BINARY_SIZE = 80
# https://github.com/Irys-xyz/bundles is authoritative
SIG_CONFIG = {
    1: {
        "sigLength": 512,
        "pubLength": 512,
        "sigName": "arweave"
    },
    2: {
        "sigLength": 64,
        "pubLength": 32,
        "sigName": "ed25519"
    },
    3: {
        "sigLength": 65,
        "pubLength": 65,
        "sigName": "ethereum"
    },
    4: {
        "sigLength": 64,
        "pubLength": 32,
        "sigName": "solana"
    },
    5: {
        "sigLength": 64,
        "pubLength": 32,
        "sigName": "injectedAptos"
    },
    6: {
        "sigLength": 64 * 32 + 4,  # max 32 64 byte signatures, +4 for 32-bit bitmap
        "pubLength": 32 * 32 + 1,  # max 64 32 byte keys, +1 for 8-bit threshold valu
        "sigName": "multiAptos"
    },
    7: {
        "sigLength": 65,
        "pubLength": 42,
        "sigName": "typedEthereum",
    }

}
