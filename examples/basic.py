from irys_sdk import Builder, DataItem, sign, create_data, EthereumSigner


def demo():
    # standard (optionally 0x prefixed) hex encoded private key (like you'd get from exporting from a wallet)
    wallet = "0x..."

    client = Builder("ethereum").wallet(wallet).network("devnet")
    # optional RPC URL
    # client.rpc_url("...")
    client = client.build()
    # get the balance for the address associated with `wallet` on the `network` bundler node
    print("balance of ", client.address,
          " in atomic units (wei) :", client.get_balance())

    print("Price for 100 bytes in atomic units (wei): ", client.get_price(100))

    # fund the bundler node
    # fund_result = client.fund(2)

    # upload some data
    upload_result = client.upload(b"Hello, Irys!", tags=[
        ("test1", "test2"), ("asdfasdf", "wwwwwwwwwwwwwwwwwwwwwwwww")], anchor="28ea4edc02a04be07da77f11cb578b0a",  target="ZjQ1Y2JhNDk3Y2Y3ZGU0YzRmMjRlZDM5NDExOTMyZTU=")

    print(upload_result)

    # manually create and sign a data item
    # (not required if the above ^ upload API works for your usecase)
    signer = EthereumSigner(wallet)
    tx = create_data(bytearray(), signer, tags=[
                     ("test1", "test2"), ("asdfasdf", "wwwwwwwwwwwwwwwwwwwwwwwww")], anchor="28ea4edc02a04be07da77f11cb578b0a", target="ZjQ1Y2JhNDk3Y2Y3ZGU0YzRmMjRlZDM5NDExOTMyZTU=")
    id = sign(tx, signer)
    is_valid = DataItem.verify(tx.get_raw())
    print(tx.id)


# if __name__ == '__main__':
#     demo()
