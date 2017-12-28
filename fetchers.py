import requests

# blockchain_info = 'https://blockchain.info/ticker'
# coindesk = 'https://api.coindesk.com/v1/bpi/currentprice.json'
coinbase_template = 'https://api.coinbase.com/v2/prices/{coin}-{currency}/spot'


def get_coinbase_spot_price(coin, currency):
    response = requests.get(coinbase_template.format(coin=coin, currency=currency))
    if response.status_code == 200:
        data = response.json()
        try:
            return float(data['data']['amount'])
        except (KeyError, ValueError, IOError):
            pass
