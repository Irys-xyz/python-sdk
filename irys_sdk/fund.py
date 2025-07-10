from time import sleep
from urllib.parse import urljoin
import requests
from irys_sdk.utils import check_and_throw, confirmation_poll, get_bundler_address

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from irys_sdk.client import Uploader


class Fund:
    irys: "Uploader"

    def __init__(self, irys):
        self.irys = irys

    def submit_transaction(self, tx_id: str):
        submit_url = urljoin(
            self.irys.url, "/account/balance/{}".format(self.irys.token))
        for _i in range(0, 4, 1):
            try:
                res = requests.post(submit_url, json={'tx_id': tx_id})
                check_and_throw(res, "submitting fund tx")
                return res
            except:
                sleep(2)
                pass
        raise Exception("Node was unable to confirm tx {}".format(tx_id))

    def fund(self, amount: int, multiplier=1.0):
        to = get_bundler_address(self.irys.url, self.irys.token_name)
        tx = self.irys.token.create_tx(amount, to)
        send_res = self.irys.token.send_tx(tx)
        tx_id = tx["tx_id"] if "tx" in tx else send_res  # type: ignore
        confirmation_poll(self.irys, tx_id)
        self.submit_transaction(tx_id)
        return send_res
