from time import sleep
from urllib.parse import urljoin
from warnings import warn

import requests


def get_balance(url: str, token: str, address: str):
    balance_url = urljoin(
        url, "/account/balance/{}?address={}".format(token, address))
    res = requests.get(balance_url)
    check_and_throw(res, "getting balance")
    return int(res.json()["balance"])


def get_price(url: str, token: str, bytes: int):
    balance_url = urljoin(
        url, "/price/{}/{}".format(token, str(bytes)))
    res = requests.get(balance_url)
    check_and_throw(res, "getting price")
    return int(res.text)


def get_bundler_address(url: str, token: str):
    res = requests.get(url)
    check_and_throw(res, "getting price")
    return res.json()["addresses"][token]


def confirmation_poll(irys, tx_id):
    # TODO @JesseTheRobot - impl proper tx conf checking logic
    for _i in range(1, 60, 1):
        try:
            return irys.token.get_tx(tx_id)
        except:
            pass
        sleep(0.5)
    warn("unable to confirm tx {} in 30s".format(tx_id))
    return


def check_and_throw(response, context="unknown", exceptions=[]):
    if response.status_code in exceptions:
        return
    if response.status_code != 200:
        raise Exception("HTTP Error while {} : {} - {}".format(context,
                                                               response.status_code, response.content))
