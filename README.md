# Irys Python SDK

This is a simple package which enables you to interact with Irys through bundlers and gateways.


## Usage

### Create & post transaction
```py
from irys.transaction import create_transaction

signer=

tx = create_transaction(
    data="Hello World"
    tags=["<Tag-Name>", "<Tag-Value>"]
)

tx.sign()

tx.upload(url="https://mainnet.irys.xyz")
```

### Download data

```py
import requests

response = requests.get("https://mainnet.irys.xyz/<txID>")

print(response.text) # "Hello world"
```