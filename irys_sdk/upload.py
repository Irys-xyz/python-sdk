
from urllib.parse import urljoin
import requests
from random import randbytes

from irys_sdk.bundle.dataitem import DataItem
from irys_sdk.bundle.tags import Tags
from irys_sdk.bundle.create import create_data
from irys_sdk.bundle.sign import sign

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from irys_sdk.client import Uploader


class Upload:
    irys: "Uploader"

    def __init__(self, irys: "Uploader"):
        self.irys = irys
        self.url = irys.url

    def upload_tx(self, tx: DataItem, **upload_opts):
        post_url = urljoin(self.url, "/tx/{}".format(self.irys.token_name))
        response = requests.post(post_url, data=tx.get_raw(), headers={
                                 "content-type": "application/octet-stream"})
        match response.status_code:
            case 429:
                raise Exception("Insufficient funds for the upload")
            case 200:
                return response.json()
            case _:
                raise Exception(
                    "Unexpected status code {} - {}".format(response.status_code, response.content))

    def upload(self, data: bytearray, tags: Tags = None, target: str = None, anchor: str = None, **upload_opts):
        signer = self.irys.token.get_signer()
        tx = create_data(data, signer, tags, target,
                         anchor if anchor else randbytes(16).hex())
        sign(tx, signer)
        if not tx.is_valid():
            raise Exception("internal error - produced data item is invalid")

        return self.upload_tx(tx, **upload_opts)
