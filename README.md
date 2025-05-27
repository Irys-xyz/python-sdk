# Irys Network Python SDK

This is a simple package which enables you to interact with the Irys Network through bundlers and gateways.


## Usage

For a full basic example, see [examples/basic.py](./examples/basic.py)

### Build the client
```py
from irys_sdk import Builder

client = Builder("ethereum").wallet("...").build()
# wallet is the only required argument, but there are others i.e rpc_url("...") to set a custom RPC URL
```

### Funding the node
Nodes work on a deposit based system, to see how much you'd need to upload some data, use `client.get_price(<size_in_bytes>)`
```py
balance = client.balance() # 100
tx_id = client.fund(10000) # in wei/atomic units
balance = client.balance() # 10100
```

### Withdrawing funds
Not currently supported in this SDK - use the JS CLI/SDK to withdraw funds

### Uploading data
```py
res = client.upload(b"hello, world!", tags=[("tag_name", "tag_value")])
print(res) # { 'id': "...", ...}
```

### Retrieving data
Make a GET request in the client of your choice to 
`https://gateway.irys.xyz/<transaction_id>`

to see transaction metadata (tags, signature, owner), GET:
`https://gateway.irys.xyz/tx/<transaction_id>`


### Contributing

This package is developed with [poetry](https://python-poetry.org/docs/)

install poetry: `pipx install poetry` \
active the venv: `poetry shell` or use `poetry run <command>` \
install dependencies: `poetry install`

